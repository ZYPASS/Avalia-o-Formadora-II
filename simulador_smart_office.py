
import pandas as pd
import numpy as np

def gerar_dados_smart_office(
    inicio="2025-01-01 00:00:00",
    dias=7,
    freq="15min",
    seed=42
) -> pd.DataFrame:
    """
    Gera um dataset simulado para sensores de um Smart Office.

    Colunas:
      - timestamp (datetime)
      - sensor_id (str)  -> ['temperatura', 'luminosidade', 'ocupacao']
      - valor (float|int)

    Regras:
      - 3 tipos de sensores
      - Janela de 7 dias, registros a cada 15 min
      - Padrões realistas: noite/dia, fins de semana, horário comercial
    """
    rng = np.random.default_rng(seed)
    idx = pd.date_range(start=pd.Timestamp(inicio), periods=int((pd.Timedelta(days=dias) / pd.Timedelta(freq))) , freq=freq)
    # Garante que o intervalo inclua o último instante do período
    if idx[-1] < pd.Timestamp(inicio) + pd.Timedelta(days=dias) - pd.Timedelta(freq):
        idx = idx.append(idx[-1] + pd.Timedelta(freq))

    registros = []

    for ts in idx:
        hora = ts.hour
        minuto = ts.minute
        weekday = ts.weekday()  # 0=segunda, 6=domingo

        # ----- Temperatura (°C) -----
        # Base diária com leve variação senoidal: mais quente no meio do dia, mais frio à noite
        # média entre 20 (noite) e 24.5 (pico diurno)
        diurno = 1 if 8 <= hora <= 18 else 0
        base_temp = 22 + 2.5 * np.sin(((hora * 60 + minuto) / (24*60)) * 2 * np.pi)  # -2.5 a +2.5
        ruido_temp = rng.normal(0, 0.8)
        temperatura = round(base_temp + (0.8 if diurno else -0.3) + ruido_temp, 2)

        # ----- Luminosidade (lux) -----
        # Zero de noite; durante o dia, varia com pico por volta de 12-14h
        if 7 <= hora <= 18:
            # curva suave com pico no meio do dia
            frac_dia = (hora - 7) / (18 - 7)
            curva = np.sin(np.pi * frac_dia)  # 0->1->0
            media_lux = 700 * curva + 200  # entre ~200 e ~900
            luminosidade = max(0, rng.normal(media_lux, 60))
        else:
            luminosidade = 0.0
        luminosidade = round(float(luminosidade), 2)

        # ----- Ocupação (0/1) -----
        # Alta probabilidade em horário comercial de dias úteis, baixa fora
        if weekday < 5 and 8 <= hora <= 18:
            p_ocup = 0.75
            # pico entre 10h e 16h
            if 10 <= hora <= 16:
                p_ocup = 0.85
            # horário de almoço reduz ligeiramente
            if 12 <= hora <= 13:
                p_ocup = 0.65
        else:
            p_ocup = 0.1

        ocupacao = int(rng.random() < p_ocup)

        # Registrar 3 leituras, uma por sensor
        registros.append((ts, "temperatura", temperatura))
        registros.append((ts, "luminosidade", luminosidade))
        registros.append((ts, "ocupacao", ocupacao))

    df = pd.DataFrame(registros, columns=["timestamp", "sensor_id", "valor"]).sort_values("timestamp").reset_index(drop=True)
    return df

if __name__ == "__main__":
    df = gerar_dados_smart_office()
    df.to_csv("smart_office_data.csv", index=False)
    print(f"Gerado smart_office_data.csv com {len(df)} linhas e {df['timestamp'].nunique()} timestamps.")

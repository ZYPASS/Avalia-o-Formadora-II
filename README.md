
# Smart Office – Dados Simulados

Este repositório contém:
- `simulador_smart_office.py`: script em Python que gera o dataset de sensores simulados.
- `smart_office_data.csv`: dataset gerado com 7 dias de leituras a cada 15 minutos, para 3 sensores (`temperatura`, `luminosidade`, `ocupacao`).

## Como rodar localmente

1. Crie e ative um ambiente (opcional, mas recomendado):
   ```bash
   python -m venv .venv
   # Windows
   .venv\\Scripts\\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

2. Instale dependências (apenas `pandas` é necessário; `numpy` já é padrão para a simulação):
   ```bash
   pip install pandas numpy
   ```

3. Rode o simulador para gerar/atualizar o CSV:
   ```bash
   python simulador_smart_office.py
   ```

O script grava `smart_office_data.csv` no mesmo diretório.

## Esquema do CSV

| coluna     | tipo      | descrição                                                |
|------------|-----------|----------------------------------------------------------|
| timestamp  | datetime  | data/hora do registro (intervalos de 15 min)            |
| sensor_id  | string    | um de: `temperatura`, `luminosidade`, `ocupacao`        |
| valor      | float/int | valor medido (°C para temperatura, lux para luz, 0/1 ocupação) |

## Observações de modelagem
- Temperatura: padrão diurno/nocturno com leve ruído gaussiano.
- Luminosidade: 0 à noite; pico no meio do dia (curva suave).
- Ocupação: maior probabilidade em dias úteis no horário comercial; menor fora desses períodos.

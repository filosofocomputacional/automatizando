import os
from datetime import datetime
from zoneinfo import ZoneInfo

# Dicionário de cidades das Américas e seus fusos horários
CIDADES = {
    "São Paulo": "America/Sao_Paulo",
    "Nova York": "America/New_York",
    "Buenos Aires": "America/Argentina/Buenos_Aires",
    "Cidade do México": "America/Mexico_City",
    "Bogotá": "America/Bogota",
    "Santiago": "America/Santiago",
    "Los Angeles": "America/Los_Angeles",
    "Lima": "America/Lima"
}

# Lê a cidade informada ou usa 'São Paulo' como padrão
NOME_CIDADE = os.environ.get("CIDADE_ESCOLHIDA", "São Paulo")
FUSO_HORARIO = CIDADES.get(NOME_CIDADE, "America/Sao_Paulo")

# Captura a hora exata no fuso horário da cidade
agora = datetime.now(ZoneInfo(FUSO_HORARIO))
data_hora_formatada = agora.strftime("%d/%m/%Y às %H:%M:%S")

linha_log = f"[{data_hora_formatada}] Cidade: {NOME_CIDADE} (Fuso: {FUSO_HORARIO})\n"

ARQUIVO_LOG = "registro_horarios.txt"

# Anexa o registro ao arquivo TXT
with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
    f.write(linha_log)

print(f"[OK] Registro salvo: {linha_log.strip()}")
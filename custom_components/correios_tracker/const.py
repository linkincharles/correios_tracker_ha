"""Constantes do Correios Tracker."""

DOMAIN = "correios_tracker"
DEFAULT_UPDATE_INTERVAL = 90  # minutos

CONF_API_KEY = "api_key"
CONF_TRACKING_CODE = "tracking_code"
CONF_DESCRIPTION = "description"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_PACKAGES = "packages"

#TROCA DO FORNECEDOR DE API DO SEU RASTREIO PARA O LINK&TRACK.
#SEURASTREIO_API_URL = "https://seurastreio.com.br/api/public/rastreio/{codigo}"
# Altere a URL da API para o Link&Track
TRACKER_API_URL = "https://api.linketrack.com/track/json?user={user}&token={token}&codigo={codigo}"

DELIVERED_STATUSES = [
    "entregue ao destinatário",
    "objeto entregue",
    "entregue",
]

ATTR_TRACKING_CODE = "codigo_objeto"
ATTR_DESCRIPTION = "descricao"
ATTR_LAST_UPDATE = "ultima_atualizacao"
ATTR_LOCATION = "localizacao"
ATTR_EVENTS = "movimentacoes"

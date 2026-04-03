"""Inicialização da integração com atualização em tempo real (Reload sem falhas)."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN, CONF_PACKAGES, CONF_API_KEY, CONF_SCAN_INTERVAL, DEFAULT_UPDATE_INTERVAL
from .coordinator import CorreiosDataCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "binary_sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configura o Correios Tracker a partir de uma entrada de configuração."""
    hass.data.setdefault(DOMAIN, {})
    
    coordinators = {}
    
    # Busca os dados (suporta o fallback das opções para a configuração base)
    api_key = entry.data.get(CONF_API_KEY)
    packages = entry.options.get(CONF_PACKAGES, entry.data.get(CONF_PACKAGES, []))
    
    for pkg in packages:
        tracking_code = pkg["tracking_code"]
        coordinator = CorreiosDataCoordinator(
            hass,
            tracking_code=tracking_code,
            description=pkg.get("description", tracking_code),
            api_key=api_key,
            scan_interval=pkg.get(CONF_SCAN_INTERVAL, DEFAULT_UPDATE_INTERVAL)
        )
        await coordinator.async_config_entry_first_refresh()
        coordinators[tracking_code] = coordinator
        
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinators": coordinators
    }
    
    # Carrega os sensores no Home Assistant
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Melhoria: Adiciona o ouvinte para que toda vez que você editar no painel, a integração se recarregue!
    entry.async_on_unload(entry.add_update_listener(update_listener))
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Descarrega a integração quando o utilizador a remove."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Disparado automaticamente quando um pacote é editado, adicionado ou removido pelo Menu."""
    _LOGGER.info("Opções do Correios Tracker atualizadas. A recarregar a integração...")
    await hass.config_entries.async_reload(entry.entry_id)
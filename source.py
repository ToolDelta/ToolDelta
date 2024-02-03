from typing import Callable, Type, Any, Tuple, NoReturn
from ujson import JSONDecodeError
from ToolDelta.packets import Packet_CommandOutput
from io import TextIOWrapper
import threading
import ToolDelta.fbconn as fbconn

VERSION = tuple[int, int, int]

def Receiver(cls):
    return cls()

class _Print:
    INFO_NORMAL = "§f 信息 "
    INFO_WARN = "§6 警告 "
    INFO_ERROR = "§4 报错 "
    INFO_FAIL = "§c 失败 "
    INFO_SUCC = "§a 成功 "
    INFO_LOAD = "§d 加载 "
    def colormode_replace(self, text: str, showmode = 0):...
    def print_with_info(self, text: str, info: str, **print_kwargs):...
    def print_err(self, text: str, **print_kwargs):"输出报错信息"
    def print_inf(self, text: str, **print_kwargs):"输出一般信息"
    def print_suc(self, text: str, **print_kwargs):"输出成功信息"
    def print_war(self, text: str, **print_kwargs):"输出警告信息"
    def fmt_info(self, text: str, info: str) -> str:...;"按照[INFO]的格式返回PRINT字符串"

class Builtins:
    class SimpleJsonDataReader:
        class DataReadError(JSONDecodeError):...
        @staticmethod
        def SafeJsonDump(obj: str | dict | list, fp: TextIOWrapper | str):...
        @staticmethod
        def SafeJsonLoad(fp: TextIOWrapper | str) -> dict:...
        @staticmethod
        def readFileFrom(plugin_name: str, file: str, default: dict | None = None) -> Any:...;"读取插件的json数据文件, 如果没有, 则新建一个空的"
        @staticmethod
        def writeFileTo(plugin_name: str, file: str, obj):"写入插件的json数据文件"
    class ArgsReplacement:
        def __init__(self, kw: dict[str, Any]):...
        def replaceTo(self, __sub: str) -> str:...
    class TMPJson:
        @staticmethod
        def loadPathJson(path: str, needFileExists: bool = True):"初始化一个json文件路径, 之后可对其进行读取和写入, 速度快"
        @staticmethod
        def unloadPathJson(path: str):"卸载一个json文件路径, 之后不可对其进行读取和写入"
        @staticmethod
        def read(path: str) -> Any:"读取json文件路径缓存的信息"
        @staticmethod
        def write(path: str, obj: Any):"向该json文件路径写入信息并缓存, 一段时间或系统关闭时会将其写入磁盘内"
        @staticmethod
        def cancel_change(path):...
    @staticmethod
    def SimpleFmt(kw: dict[str, Any], __sub: str) -> str:...
    @staticmethod
    def simpleAssert(cond: Any, exc):...
    @staticmethod
    def try_int(arg) -> int | None:...
    @staticmethod
    def add_in_dialogue_player(player: str):...
    @staticmethod
    def remove_in_dialogue_player(player: str):...
    @staticmethod
    def player_in_dialogue(player: str) -> bool:...
    @staticmethod
    def create_dialogue_threading(player, func, exc_cb = None, args = (), kwargs = {}):...

class Frame:
    class ThreadExit(SystemExit):...
    class SystemVersionException(OSError):...
    class FrameBasic:
        system_version: VERSION
        max_connect_fb_time: int
        connect_fb_start_time: int
        data_path: str
    class ClassicThread(threading.Thread):
        def __init__(self, func: Callable, args: tuple = (), **kwargs):...
        def run(self):...
        def get_id(self):...
        def stop(self):...
    def __init__(self):...
    def get_game_control(self):
        return GameManager(Frame())
    def getFreePort(self, start = 8080, usage = "none") -> int | None:...
    def add_console_cmd_trigger(
            self,
            triggers: list[str],
            arg_hint: str | None,
            usage: str,
            func: Callable[[list[str]], None]
        ):...
    sys_data: FrameBasic
    createThread = ClassicThread

class GameManager:
    players_uuid = {}
    allplayers = []
    bot_name = ""
    linked_frame: Frame
    def __init__(self, frame: Frame):
        self.linked_frame = frame
    def sendwocmd(self, cmd: str):...
    def sendcmd(self, cmd: str, waitForResp: bool = False, timeout: int = 30) -> bytes | Packet_CommandOutput:...
    def sendwscmd(self, cmd: str, waitForResp: bool = False, timeout: int = 30) -> bytes | Packet_CommandOutput:...
    def sendfbcmd(self, cmd: str):...
    def sendPacket(self, pktType: int, pkt: dict):...
    def sendPacketBytes(self, pkt: bytes):...
    def say_to(self, target: str, msg: str):
        self.sendwocmd("tellraw " + target + ' {"rawtext":[{"text":"' + msg + '"}]}')
    def player_title(self, target: str, text: str):
        self.sendwocmd(f"title {target} title {text}")
    def player_subtitle(self, target: str, text: str):
        self.sendwocmd(f"title {target} subtitle {text}")
    def player_actionbar(self, target: str, text: str):
        self.sendwocmd(f"title {target} actionbar {text}")

class Plugin:
    name = "<未命名插件>"
    version = (0, 0, 1)
    author = "?"
    require_listen_packets = []
    dotcs_old_type = False
    def __init__(self, frame: Frame):
        self.frame = frame

class PluginAPI:
    name = "<未命名api>"
    version = (0, 0, 1)

class PluginGroup:
    class PluginAPINotFoundError(ModuleNotFoundError):
        def __init__(self, name):...
    class PluginAPIVersionError(ModuleNotFoundError):
        def __init__(self, name, m_ver, n_ver):...
    plugins: list[Plugin] = []
    plugins_funcs: dict[str, list]
    linked_frame: Frame
    packet_funcs: dict[str, list[Callable]] = {}
    PRG_NAME = ""
    @staticmethod
    def get_plugin_api(apiName: str, min_version: tuple | None = None) -> PluginAPI | NoReturn:...
    def add_plugin(self, plugin: Type[Plugin]) -> Plugin:... # type: ignore
    def add_plugin_api(self, apiName: str) -> Receiver:... # type: ignore
    def add_plugin_as_api(self, apiName: str) -> Receiver:... # type: ignore
    def add_packet_listener(self, pktID) -> Receiver:... # type: ignore
    @staticmethod
    def checkSystemVersion(need_vers: VERSION):...

class Cfg:
    "配置文件检测类"
    class Group:
        "json键组"
        def __init__(self, *keys):...
        def __repr__(self) -> str:...
    class UnneccessaryKey:
        "非必须的json键"
        def __init__(self, key):...
        def __repr__(self) -> str:...
    class ConfigError(Exception):
        def __init__(self, errStr: str, errPos: list):...
    class ConfigKeyError(ConfigError):...
    class ConfigValueError(ConfigError):...
    class VersionLowError(ConfigError):...
    class PInt(int):"正整数"
    class NNInt(int):"非负整数"
    class PFloat(float):"正浮点小数"
    class NNFloat(float):"非负浮点小数"
    class PNumber:"正数"
    class NNNumber:"大于0的数"

    def get_cfg(self, path: str, standard_type: dict):...
    def default_cfg(self, path: str, default: dict, force: bool = False):...
    def exists(self, path: str):...
    def checkDict(self, patt: dict, cfg: dict, __nowcheck: list = []):...
    def checkList(self, patt, lst: list, __nowcheck: list = []):...
    def getPluginConfigAndVersion(self, pluginName: str, standardType: dict, default: dict, default_vers: VERSION) -> Tuple[dict, VERSION]:...

plugins: PluginGroup
Config: Cfg
Print: _Print
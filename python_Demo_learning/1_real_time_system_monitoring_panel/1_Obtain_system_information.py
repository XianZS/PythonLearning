# 基于psutil获取系统信息
from annotationlib import get_annotate_from_class_namespace
import psutil
import os
import time
from datetime import datetime

def get_process_top(n=8):
    # 审讯所有的进程，按照内存占用率进行排序，返回前n个
    procs=[]
    for p in psutil.process_iter(["name","memory_info","cpu_percent"]):
        try:
            name=p.info["name"][:20]
            mem_mb=p.info["memory_info"].rss/1024/1024
            cpu_pct=p.info["cpu_percent"] or 0
            procs.append((name,cpu_pct,mem_mb))
        except (psutil.NoSuchProcess,psutil.AccessDenied) as e:
            print(f"[Error]:{e}")
        except Exception as e:
            print(f"[Exception]:{e}")
    procs.sort(key=lambda x:x[2],reverse=True)
    return procs[:n]

def get_battery():
    # 审讯电池，判断电池剩余电量，是否处于持续充电状态
    try:
        bat=psutil.sensors_battery()
        if bat:
            status="充电中" if bat.power_plugged else "放电中"
            return f"{status} | {bat.percent:.0f}%"
        else:
            pass
    except Exception as e:
        print(f"[Error]:{e}")
        return None

def get_temp():
    # 审讯温度
    try:
        temps=psutil.sensors_temperatures() # type:ignore
        if not temps:
            return None
        for name in ["coretemp","k10temp","cpu_thermal","acpitz"]:
            if name in temps and temps[name]:
                return temps[name][0].current
            else:
                return None
        frist=next(iter(temps.values()))
        if first:
            return first[0].current
    except Exception:
        pass
    return None



while True:
    os.system("cls" if os.name=="nt" else "clear")
    # 审视CPU西悉尼
    cpu=psutil.cpu_percent(interval=0.5)
    per_cpi=psutil.cpu_percent(interval=0,percpu=True)
    cpu_frep=psutil.cpu_freq()  # 当前主频
    cpu_count_logical=psutil.cpu_count()    # 逻辑核心数
    cpu_count_physical=psutil.cpu_count(logical=True)   # 物理核心数
    mem=psutil.virtual_memory()
    swap=psutil.swap_memory()
    disk=psutil.disk_usage("/")
    disk_io=psutil.disk_io_counters()
    net=psutil.net_io_counters()
    cpu_temp=get_temp()
    battery=get_battery()
    boot_time=datetime.fromtimestamp(psutil.boot_time())
    print(f"=== 系统监控面板 ===")
    print(f"[系统启动时间]:{boot_time.strftime("%Y-%m-%d %H:%M:%S")}")
    print(f"[CPU使用率]:{cpu}%")
    if cpu_frep:
        print(f"[CPU主频]:{cpu_frep}MHZ")
    print(f"[CPU核心数]:{cpu_count_physical}物理/{cpu_count_logical}逻辑")
    time.sleep(1)








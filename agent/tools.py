import docker
from docker.errors import NotFound
from typing import Dict, Any, Optional

client = docker.from_env()

def get_server_stats(container_name: str) -> Dict[str, Any]:
    """
    Get CPU and Memory usage statistics for a container.
    """
    try:
        container = client.containers.get(container_name)
        stats = container.stats(stream=False)
        
        # Calculate memory usage in MB
        # 'usage' might not be available in all docker ver/OS, but standard assumption
        memory_usage = stats.get('memory_stats', {}).get('usage', 0) / (1024 * 1024)
        
        # Calculate CPU usage (simplified approximation)
        cpu_usage = 0.0
        cpu_stats = stats.get('cpu_stats', {})
        precpu_stats = stats.get('precpu_stats', {})
        
        if cpu_stats and precpu_stats:
            cpu_delta = cpu_stats.get('cpu_usage', {}).get('total_usage', 0) - precpu_stats.get('cpu_usage', {}).get('total_usage', 0)
            system_cpu_delta = cpu_stats.get('system_cpu_usage', 0) - precpu_stats.get('system_cpu_usage', 0)
            
            if system_cpu_delta > 0:
                percpu_usage = cpu_stats.get('cpu_usage', {}).get('percpu_usage', [])
                if percpu_usage:
                    cpu_usage = (cpu_delta / system_cpu_delta) * len(percpu_usage) * 100.0
                else:
                    # Fallback if percpu_usage is not available
                    cpu_usage = (cpu_delta / system_cpu_delta) * 100.0

        return {
            "status": container.status,
            "memory_mb": round(memory_usage, 2),
            "cpu_percent": round(cpu_usage, 2)
        }
    except NotFound:
        return {"error": f"Container '{container_name}' not found."}
    except Exception as e:
        return {"error": str(e)}

def get_server_logs(container_name: str) -> str:
    """
    Get the last 20 lines of logs from a container.
    """
    try:
        container = client.containers.get(container_name)
        logs = container.logs(tail=20).decode('utf-8')
        return logs
    except NotFound:
        return f"Container '{container_name}' not found."
    except Exception as e:
        return f"Error retrieving logs: {str(e)}"

def restart_server(container_name: str) -> str:
    """
    Restart a container.
    """
    try:
        container = client.containers.get(container_name)
        container.restart()
        return f"Container '{container_name}' restarted successfully."
    except NotFound:
        return f"Container '{container_name}' not found."
    except Exception as e:
        return f"Error restarting container: {str(e)}"

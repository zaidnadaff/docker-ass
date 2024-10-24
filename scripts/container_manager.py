import docker
import time
import sys
from datetime import datetime

class ContainerManager:
    def __init__(self):
        self.client = docker.from_env()
        self.container_name = "streamlit_app"

    def get_container_stats(self, container):
        """Get container resource usage statistics"""
        stats = container.stats(stream=False)
        cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
        memory_usage = stats['memory_stats']['usage']
        return {
            'cpu': cpu_usage,
            'memory': memory_usage / (1024 * 1024)  # Convert to MB
        }

    def monitor_container(self):
        try:
            container = self.client.containers.get(self.container_name)
            stats = self.get_container_stats(container)
            print(f"\nContainer: {container.name}")
            print(f"Status: {container.status}")
            print(f"CPU Usage: {stats['cpu']}")
            print(f"Memory Usage: {stats['memory']:.2f} MB")
            return container.status == 'running'
        except docker.errors.NotFound:
            print(f"Container {self.container_name} not found")
            return False
        except Exception as e:
            print(f"Error monitoring container: {e}")
            return False

    def restart_container(self):
        """Restart the container if it's unhealthy"""
        try:
            container = self.client.containers.get(self.container_name)
            print(f"Restarting container {self.container_name}...")
            container.restart()
            print("Container restarted successfully")
        except docker.errors.NotFound:
            print(f"Container {self.container_name} not found")
        except Exception as e:
            print(f"Error restarting container: {e}")

    def list_all_containers(self):
        """List all containers and their status"""
        print("\nAll Containers:")
        print("-" * 50)
        for container in self.client.containers.list(all=True):
            print(f"Name: {container.name}")
            print(f"Status: {container.status}")
            print(f"Image: {container.image.tags[0] if container.image.tags else 'none'}")
            print("-" * 50)

    def log_container_events(self):
        """Log container events"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"container_log_{timestamp}.txt", "a") as log_file:
            log_file.write(f"Container monitoring started at {timestamp}\n")
            while True:
                status = self.monitor_container()
                log_file.write(f"{datetime.now()}: Status - {status}\n")
                log_file.flush()
                time.sleep(30)

def main():
    manager = ContainerManager()
    
    print("Container Management System")
    print("1. Monitor container")
    print("2. List all containers")
    print("3. Restart container")
    print("4. Start continuous monitoring")
    print("5. Exit")

    while True:
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            manager.monitor_container()
        elif choice == '2':
            manager.list_all_containers()
        elif choice == '3':
            manager.restart_container()
        elif choice == '4':
            try:
                manager.log_container_events()
            except KeyboardInterrupt:
                print("\nMonitoring stopped by user")
        elif choice == '5':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
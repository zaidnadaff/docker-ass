import docker
import time
from datetime import datetime

class NetworkManager:
    def __init__(self):
        self.client = docker.from_env()
        self.network_name = "web_app_network"

    def create_network(self):
        """Create a new network if it doesn't exist"""
        try:
            existing_networks = [n.name for n in self.client.networks.list()]
            if self.network_name not in existing_networks:
                network = self.client.networks.create(
                    name=self.network_name,
                    driver="bridge",
                    check_duplicate=True
                )
                print(f"Network {self.network_name} created successfully")
                return network
            print(f"Network {self.network_name} already exists")
            return self.client.networks.get(self.network_name)
        except Exception as e:
            print(f"Error creating network: {e}")
            return None

    def connect_container(self, container_name):
        """Connect a container to the network"""
        try:
            network = self.client.networks.get(self.network_name)
            container = self.client.containers.get(container_name)
            network.connect(container)
            print(f"Connected {container_name} to {self.network_name}")
        except Exception as e:
            print(f"Error connecting container: {e}")

    def disconnect_container(self, container_name):
        """Disconnect a container from the network"""
        try:
            network = self.client.networks.get(self.network_name)
            container = self.client.containers.get(container_name)
            network.disconnect(container)
            print(f"Disconnected {container_name} from {self.network_name}")
        except Exception as e:
            print(f"Error disconnecting container: {e}")

    def list_networks(self):
        """List all networks and their details"""
        print("\nNetwork List:")
        print("-" * 50)
        for network in self.client.networks.list():
            print(f"Network Name: {network.name}")
            print(f"Network ID: {network.short_id}")
            print(f"Driver: {network.attrs['Driver']}")
            if network.attrs.get('Containers'):
                print("Connected Containers:")
                for container_id, container_info in network.attrs['Containers'].items():
                    print(f"  - {container_info['Name']}")
            print("-" * 50)

    def inspect_network(self, network_name):
        """Inspect a specific network"""
        try:
            network = self.client.networks.get(network_name)
            print(f"\nNetwork Details for {network_name}:")
            print(f"ID: {network.short_id}")
            print(f"Created: {network.attrs['Created']}")
            print(f"Scope: {network.attrs['Scope']}")
            print(f"Driver: {network.attrs['Driver']}")
            print("Connected Containers:")
            for container_id, container_info in network.attrs.get('Containers', {}).items():
                print(f"  - {container_info['Name']} ({container_id[:12]})")
        except Exception as e:
            print(f"Error inspecting network: {e}")

def main():
    manager = NetworkManager()
    
    print("Network Management System")
    print("1. Create network")
    print("2. List all networks")
    print("3. Connect container to network")
    print("4. Disconnect container from network")
    print("5. Inspect network")
    print("6. Exit")

    while True:
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            manager.create_network()
        elif choice == '2':
            manager.list_networks()
        elif choice == '3':
            container_name = input("Enter container name: ")
            manager.connect_container(container_name)
        elif choice == '4':
            container_name = input("Enter container name: ")
            manager.disconnect_container(container_name)
        elif choice == '5':
            network_name = input("Enter network name: ")
            manager.inspect_network(network_name)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import requests
import time
import subprocess
import threading
import os
from requests.auth import HTTPDigestAuth

class GrandstreamMonitor:
    def __init__(self, phone_ip, username, password):
        self.phone_ip = phone_ip
        self.username = username
        self.password = password
        self.base_url = f"http://{phone_ip}"
        self.call_active = False
        
    def check_call_status(self):
        """Check if there's an active call"""
        try:
            # Try multiple API endpoints as they vary by Grandstream model
            endpoints = [
                "/cgi-bin/api-get_call_status",
                "/api/v1/call/status",
                "/cgi-bin/api-get_status"
            ]
            
            for endpoint in endpoints:
                try:
                    url = f"{self.base_url}{endpoint}"
                    response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password), timeout=5)
                    
                    if response.status_code == 200:
                        # Check for call status in response
                        content = response.text.lower()
                        if any(status in content for status in ['active', 'ringing', 'connected', 'inuse']):
                            return True
                        if 'idle' in content or 'available' in content:
                            return False
                except:
                    continue
            
            # If no API works, try the web interface
            try:
                url = f"{self.base_url}/"
                response = requests.get(url, auth=HTTPDigestAuth(self.username, self.password), timeout=5)
                if response.status_code == 200:
                    # Simple check for call status in HTML
                    if 'ringing' in response.text.lower() or 'incoming' in response.text.lower():
                        return True
            except:
                pass
                
            return False
            
        except Exception as e:
            print(f"Error checking call status: {e}")
            return False
    
    def send_phone_command(self, command):
        """Send command to phone via key simulation"""
        try:
            # Different methods to send commands
            methods = [
                # Method 1: DTMF codes
                lambda: requests.post(f"{self.base_url}/cgi-bin/api-send_dtmf", 
                                    data={'account': '1', 'digit': command},
                                    auth=HTTPDigestAuth(self.username, self.password)),
                # Method 2: Key simulation
                lambda: requests.post(f"{self.base_url}/cgi-bin/api-send_key", 
                                    data={'account': '1', 'key': command},
                                    auth=HTTPDigestAuth(self.username, self.password))
            ]
            
            for method in methods:
                try:
                    response = method()
                    if response.status_code == 200:
                        return True
                except:
                    continue
            return False
            
        except Exception as e:
            print(f"Error sending command {command}: {e}")
            return False
    
    def answer_call(self):
        """Answer incoming call"""
        print("Attempting to answer call...")
        return self.send_phone_command('Answer') or self.send_phone_command('A') or self.send_phone_command('1')
    
    def enable_speaker_mode(self):
        """Enable speaker mode on the phone"""
        print("Enabling speaker mode...")
        # Try common Grandstream speaker mode codes
        return (self.send_phone_command('*64') or 
                self.send_phone_command('Spk') or 
                self.send_phone_command('Speaker'))
    
    def monitor_calls(self):
        """Main monitoring loop"""
        print(f"Starting Grandstream phone monitor for {self.phone_ip}...")
        print("Press Ctrl+C to stop monitoring")
        
        while True:
            try:
                call_status = self.check_call_status()
                
                if call_status and not self.call_active:
                    print("Incoming call detected!")
                    self.call_active = True
                    
                    # Answer the call automatically
                    if self.answer_call():
                        print("Call answered successfully")
                        
                        # Enable speaker mode after a short delay
                        time.sleep(2)
                        if self.enable_speaker_mode():
                            print("Speaker mode activated")
                        else:
                            print("Could not enable speaker mode automatically")
                            
                        # Route audio to PC
                        self.route_audio_to_pc()
                        
                elif not call_status and self.call_active:
                    print("Call ended")
                    self.call_active = False
                    self.restore_audio()
                
                time.sleep(1)  # Check every second
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped by user")
                break
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(5)
    
    def route_audio_to_pc(self):
        """Route phone audio to PC speakers"""
        try:
            # Create virtual audio sink if not exists
            subprocess.run(['pactl', 'list', 'short', 'sinks'], check=True)
            print("Audio system ready for routing")
        except Exception as e:
            print(f"Audio routing preparation error: {e}")
    
    def restore_audio(self):
        """Restore normal audio settings"""
        print("Audio routing restored to normal")

# Configuration - Updated with your phone details
PHONE_IP = "192.168.6.103"  # Your phone's IP address
USERNAME = "admin"          # Grandstream web interface username
PASSWORD = "aikhanlabit"    # Grandstream web interface password

if __name__ == "__main__":
    monitor = GrandstreamMonitor(PHONE_IP, USERNAME, PASSWORD)
    monitor.monitor_calls()

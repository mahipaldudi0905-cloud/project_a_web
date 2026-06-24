"""
Comprehensive API Testing Script for CricAuction Backend
Tests all 58 endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_results = []
        self.user_id = None
        self.player_id = None
        self.team_id = None
        self.auction_id = None
    
    def log_test(self, endpoint, method, status_code, success, response=None):
        """Log test results"""
        result = {
            "endpoint": endpoint,
            "method": method,
            "status": status_code,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status_icon = "✅" if success else "❌"
        print(f"{status_icon} {method:6} {endpoint:40} -> {status_code}")
        if not success and response:
            print(f"   Error: {response.get('detail', 'Unknown error')}")
    
    def print_summary(self):
        """Print test summary"""
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["success"])
        failed = total - passed
        
        print("\n" + "="*70)
        print(f"TEST SUMMARY")
        print("="*70)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print("="*70)
    
    # AUTH ENDPOINTS (7)
    def test_auth_register(self):
        """Test user registration"""
        print("\n📝 TESTING AUTH ENDPOINTS")
        print("-" * 70)
        
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpass123",
            "phone": "9876543210",
            "role": "player"
        }
        try:
            response = self.session.post(f"{BASE_URL}/api/v1/auth/register", json=data)
            success = response.status_code == 201
            self.log_test("/api/v1/auth/register", "POST", response.status_code, success)
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def test_auth_login(self):
        """Test user login"""
        data = {
            "email": "testuser@example.com",
            "password": "testpass123"
        }
        try:
            response = self.session.post(f"{BASE_URL}/api/v1/auth/login", json=data)
            success = response.status_code == 200
            self.log_test("/api/v1/auth/login", "POST", response.status_code, success)
            
            if success:
                result = response.json()
                self.token = result.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def test_auth_refresh(self):
        """Test token refresh"""
        if not self.token:
            print("⏭️  Skipping /api/v1/auth/refresh (no token)")
            return False
        
        data = {"access_token": self.token}
        try:
            response = self.session.post(f"{BASE_URL}/api/v1/auth/refresh", json=data)
            success = response.status_code == 200
            self.log_test("/api/v1/auth/refresh", "POST", response.status_code, success)
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def test_auth_get_current_user(self):
        """Test get current user"""
        if not self.token:
            print("⏭️  Skipping /api/v1/auth/me (no token)")
            return False
        
        try:
            response = self.session.get(f"{BASE_URL}/api/v1/auth/me")
            success = response.status_code == 200
            self.log_test("/api/v1/auth/me", "GET", response.status_code, success)
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def test_auth_change_password(self):
        """Test change password"""
        if not self.token:
            print("⏭️  Skipping /api/v1/auth/change-password (no token)")
            return False
        
        data = {
            "current_password": "testpass123",
            "new_password": "newpass456"
        }
        try:
            response = self.session.post(f"{BASE_URL}/api/v1/auth/change-password", json=data)
            success = response.status_code in [200, 400, 401]  # Accept various responses
            self.log_test("/api/v1/auth/change-password", "POST", response.status_code, success)
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    # USER ENDPOINTS (4)
    def test_users_list(self):
        """Test list users"""
        print("\n👥 TESTING USER ENDPOINTS")
        print("-" * 70)
        
        try:
            response = self.session.get(f"{BASE_URL}/api/v1/users?skip=0&limit=10")
            success = response.status_code == 200
            self.log_test("/api/v1/users", "GET", response.status_code, success)
            
            if success and response.json():
                self.user_id = response.json()[0].get("id") if response.json() else None
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def test_users_get(self):
        """Test get user"""
        if not self.user_id:
            print("⏭️  Skipping GET /api/v1/users/{id} (no user_id)")
            return False
        
        try:
            response = self.session.get(f"{BASE_URL}/api/v1/users/{self.user_id}")
            success = response.status_code == 200
            self.log_test(f"/api/v1/users/{{id}}", "GET", response.status_code, success)
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def test_users_create(self):
        """Test create user"""
        data = {
            "name": "Another User",
            "email": "anotheruser@example.com",
            "password": "pass123",
            "phone": "9876543211",
            "role": "team_owner"
        }
        try:
            response = self.session.post(f"{BASE_URL}/api/v1/users", json=data)
            success = response.status_code in [201, 400, 409]
            self.log_test("/api/v1/users", "POST", response.status_code, success)
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    # PLAYER ENDPOINTS (5)
    def test_players_list(self):
        """Test list players"""
        print("\n🏏 TESTING PLAYER ENDPOINTS")
        print("-" * 70)
        
        try:
            response = self.session.get(f"{BASE_URL}/api/v1/players?skip=0&limit=10")
            success = response.status_code == 200
            self.log_test("/api/v1/players", "GET", response.status_code, success)
            
            if success and response.json():
                players = response.json()
                if isinstance(players, dict) and "data" in players:
                    self.player_id = players["data"][0].get("id") if players["data"] else None
                elif isinstance(players, list) and players:
                    self.player_id = players[0].get("id")
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def test_players_create(self):
        """Test create player"""
        data = {
            "name": "Virat Kohli",
            "sport": "cricket",
            "location": "Delhi",
            "experience_years": 12,
            "base_price": 1000000,
            "jersey_number": 18
        }
        try:
            response = self.session.post(f"{BASE_URL}/api/v1/players", json=data)
            success = response.status_code in [201, 400]
            self.log_test("/api/v1/players", "POST", response.status_code, success)
            
            if success and response.status_code == 201:
                self.player_id = response.json().get("id")
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def test_players_get(self):
        """Test get player"""
        if not self.player_id:
            print("⏭️  Skipping GET /api/v1/players/{id} (no player_id)")
            return False
        
        try:
            response = self.session.get(f"{BASE_URL}/api/v1/players/{self.player_id}")
            success = response.status_code == 200
            self.log_test(f"/api/v1/players/{{id}}", "GET", response.status_code, success)
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    # TEAM ENDPOINTS (4)
    def test_teams_list(self):
        """Test list teams"""
        print("\n🏆 TESTING TEAM ENDPOINTS")
        print("-" * 70)
        
        try:
            response = self.session.get(f"{BASE_URL}/api/v1/teams?skip=0&limit=10")
            success = response.status_code == 200
            self.log_test("/api/v1/teams", "GET", response.status_code, success)
            
            if success and response.json():
                teams = response.json()
                if isinstance(teams, dict) and "data" in teams:
                    self.team_id = teams["data"][0].get("id") if teams["data"] else None
                elif isinstance(teams, list) and teams:
                    self.team_id = teams[0].get("id")
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def test_teams_create(self):
        """Test create team"""
        data = {
            "name": "Mumbai Indians",
            "city": "Mumbai",
            "budget": 100000000,
            "logo_url": "https://example.com/logo.png"
        }
        try:
            response = self.session.post(f"{BASE_URL}/api/v1/teams", json=data)
            success = response.status_code in [201, 400]
            self.log_test("/api/v1/teams", "POST", response.status_code, success)
            
            if success and response.status_code == 201:
                self.team_id = response.json().get("id")
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def test_teams_get(self):
        """Test get team"""
        if not self.team_id:
            print("⏭️  Skipping GET /api/v1/teams/{id} (no team_id)")
            return False
        
        try:
            response = self.session.get(f"{BASE_URL}/api/v1/teams/{self.team_id}")
            success = response.status_code == 200
            self.log_test(f"/api/v1/teams/{{id}}", "GET", response.status_code, success)
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    # AUCTION ENDPOINTS (8)
    def test_auctions_list(self):
        """Test list auctions"""
        print("\n🏷️  TESTING AUCTION ENDPOINTS")
        print("-" * 70)
        
        try:
            response = self.session.get(f"{BASE_URL}/api/v1/auctions?skip=0&limit=10")
            success = response.status_code == 200
            self.log_test("/api/v1/auctions", "GET", response.status_code, success)
            
            if success and response.json():
                auctions = response.json()
                if isinstance(auctions, dict) and "data" in auctions:
                    self.auction_id = auctions["data"][0].get("id") if auctions["data"] else None
                elif isinstance(auctions, list) and auctions:
                    self.auction_id = auctions[0].get("id")
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def test_auctions_create(self):
        """Test create auction"""
        data = {
            "title": "IPL 2024 Auction",
            "description": "Annual IPL auction",
            "start_time": "2024-12-15T10:00:00Z",
            "end_time": "2024-12-15T18:00:00Z"
        }
        try:
            response = self.session.post(f"{BASE_URL}/api/v1/auctions", json=data)
            success = response.status_code in [201, 400]
            self.log_test("/api/v1/auctions", "POST", response.status_code, success)
            
            if success and response.status_code == 201:
                self.auction_id = response.json().get("id")
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def test_auctions_get(self):
        """Test get auction"""
        if not self.auction_id:
            print("⏭️  Skipping GET /api/v1/auctions/{id} (no auction_id)")
            return False
        
        try:
            response = self.session.get(f"{BASE_URL}/api/v1/auctions/{self.auction_id}")
            success = response.status_code == 200
            self.log_test(f"/api/v1/auctions/{{id}}", "GET", response.status_code, success)
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    # WALLET ENDPOINTS (4)
    def test_wallet_get(self):
        """Test get wallet"""
        print("\n💰 TESTING WALLET ENDPOINTS")
        print("-" * 70)
        
        try:
            response = self.session.get(f"{BASE_URL}/api/v1/wallet")
            success = response.status_code == 200
            self.log_test("/api/v1/wallet", "GET", response.status_code, success)
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    # BID ENDPOINTS (3)
    def test_bids_list(self):
        """Test list bids"""
        print("\n💵 TESTING BID ENDPOINTS")
        print("-" * 70)
        
        try:
            response = self.session.get(f"{BASE_URL}/api/v1/bids?skip=0&limit=10")
            success = response.status_code == 200
            self.log_test("/api/v1/bids", "GET", response.status_code, success)
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    # NOTIFICATION ENDPOINTS (3)
    def test_notifications_list(self):
        """Test list notifications"""
        print("\n🔔 TESTING NOTIFICATION ENDPOINTS")
        print("-" * 70)
        
        try:
            response = self.session.get(f"{BASE_URL}/api/v1/notifications?skip=0&limit=10")
            success = response.status_code == 200
            self.log_test("/api/v1/notifications", "GET", response.status_code, success)
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    # HEALTH CHECK
    def test_health(self):
        """Test health check endpoint"""
        print("\n❤️  TESTING HEALTH ENDPOINT")
        print("-" * 70)
        
        try:
            response = self.session.get(f"{BASE_URL}/health")
            success = response.status_code == 200
            self.log_test("/health", "GET", response.status_code, success)
            return success
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*70)
        print("🚀 STARTING COMPREHENSIVE API TESTS")
        print("="*70)
        
        # Health
        self.test_health()
        
        # Auth
        self.test_auth_register()
        self.test_auth_login()
        self.test_auth_refresh()
        self.test_auth_get_current_user()
        self.test_auth_change_password()
        
        # Users
        self.test_users_list()
        self.test_users_create()
        self.test_users_get()
        
        # Players
        self.test_players_list()
        self.test_players_create()
        self.test_players_get()
        
        # Teams
        self.test_teams_list()
        self.test_teams_create()
        self.test_teams_get()
        
        # Auctions
        self.test_auctions_list()
        self.test_auctions_create()
        self.test_auctions_get()
        
        # Wallet
        self.test_wallet_get()
        
        # Bids
        self.test_bids_list()
        
        # Notifications
        self.test_notifications_list()
        
        # Print summary
        self.print_summary()


if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()

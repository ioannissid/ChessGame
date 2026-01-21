#OpeningBookAPI.py - Access free online opening databases without downloading huge files

import requests
import time
import threading
from typing import Optional, List, Tuple

class OpeningBookAPI:
    # Initialize the API client with base URL and timeout 
    # Data is fetched from Lichess opening explorer
    
    def __init__(self, timeout: int = 5):
        self.BASE_URL = "https://explorer.lichess.ovh/lichess"
        self.timeout = timeout
        
        # Create session to reuse connections (faster)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "ChessEngine/1.0",
            "Accept": "application/json"
        })
        
        # Track failed API calls to implement backoff (don't hammer server)
        self.consecutive_failures = 0
        self.MAX_FAILURES = 3
    
    def get_opening_move(self, fen: str, strategy: int = 0) -> Optional[str]:
        # Query the opening book for the best move in the given position (FEN)
        
        # Don't retry if we've had too many failures
        if self.consecutive_failures >= self.MAX_FAILURES:
            return None
        
        try:
            params = {
                "fen": fen,
                "topGames": 0,  # Don't need game list, just statistics
                "recentGames": 0  # Don't need recent games either
            }
            
            print(f"[API] Querying Lichess for opening... (strategy {strategy})")
            
            # Make the API request
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout
            )
            
            # Check if request was successful
            if response.status_code != 200:
                print(f"[API] Error: HTTP {response.status_code}")
                self.consecutive_failures += 1
                return None
            
            data = response.json()
            
            # If no moves found (position is too unusual), return None
            if not data.get("moves"):
                print("[API] No opening found in database (too rare position)")
                return None
            
            # Sort moves by popularity (total games)
            sorted_moves = sorted(
                data["moves"],
                key=lambda x: x.get("white", 0) + x.get("black", 0) + x.get("draws", 0),
                reverse=True
            )
            
            # Select move based on strategy
            if strategy == 0:
                # Most popular move
                selected_move = sorted_moves[0]
            elif strategy == 1 and len(sorted_moves) > 1:
                # Second most popular move
                selected_move = sorted_moves[1]
            elif strategy == 2 and len(sorted_moves) > 0:
                # Random from top 3 moves
                import random
                top_moves = sorted_moves[:min(3, len(sorted_moves))]
                selected_move = random.choice(top_moves)
            else:
                # Fallback to most popular
                selected_move = sorted_moves[0]
            
            # Extract the move in UCI format and optionally log statistics
            move_uci = selected_move.get("uci")
            move_san = selected_move.get("san", "?")  # Standard notation (e.g., "e4")
            
            # Print statistics for debugging
            total_games = selected_move.get("white", 0) + selected_move.get("black", 0) + selected_move.get("draws", 0)
            white_wins = selected_move.get("white", 0)
            strategy_names = ["Most Popular", "Second Popular", "Random Top 3"]
            print(f"[API] {strategy_names[strategy]}: {move_san} (UCI: {move_uci}) - Played {total_games:,} times")
            
            # Reset failure counter on success
            self.consecutive_failures = 0
            
            return move_uci
        
        except requests.Timeout:
            print("[API] Request timeout - using engine search instead")
            self.consecutive_failures += 1
            return None
        
        except requests.ConnectionError:
            print("[API] Connection error - offline or server unreachable")
            self.consecutive_failures += 1
            return None
        
        except Exception as e:
            print(f"[API] Unexpected error: {e}")
            self.consecutive_failures += 1
            return None
    
    def uci_to_internal_move(self, uci_move: str, valid_moves: List) -> Optional:
       #c Convert UCI move string (e.g., "e2e4") to my engine's MOVE object
        
        if not uci_move or len(uci_move) < 4:
            return None
        
        # Parse UCI move
        start_col = ord(uci_move[0]) - ord('a')  # Convert 'a'-'h' to 0-7
        start_row = 8 - int(uci_move[1])          # Convert '1'-'8' to 7-0
        end_col = ord(uci_move[2]) - ord('a')
        end_row = 8 - int(uci_move[3])
        
        # Find matching move in valid moves
        for move in valid_moves:
            if (move.STARTROW == start_row and
                move.STARTCOL == start_col and
                move.ENDROW == end_row and
                move.ENDCOL == end_col):
                
                # If promotion is specified (e.g., "e7e8q"), check if it matches
                if len(uci_move) > 4:
                    # For now, accept any promotion - your engine should handle this
                    pass
                
                return move
        
        print(f"[Warning] UCI move {uci_move} not found in valid moves")
        return None


def should_use_opening_book(move_count: int) -> bool:
    # Use opening book for first 30 moves only
    return move_count < 30

# Transposition Table for caching board position evaluations
# Uses hash keys to avoid re-evaluating positions already seen

class TranspositionTable:
    # Stores evaluated positions to avoid recalculating the same position multiple times. Uses Zobrist hashing (BOARD_HASH from ChessEngine) as the key. Constants for evaluation flags
    EXACT = "EXACT"              # Full alpha-beta search, real value
    LOWER_BOUND = "LOWER_BOUND"  # Beta cutoff - true value >= stored value
    UPPER_BOUND = "UPPER_BOUND"  # Alpha cutoff - true value <= stored value
    
    def __init__(self, max_size=1000000):
      
        #Initialize transposition table
        #Args:
        #    max_size: Maximum number of entries before replacement strategy kicks in
        self.table = {}
        self.max_size = max_size
        self.current_age = 0  # Incremented each move to track entry age
    
    def store(self, hash_key, depth, value, flag):
        # Args:
        #    hash_key: Zobrist hash from gamestate.BOARD_HASH
        #    depth: Search depth at which this evaluation was made
        #    value: Evaluated score for the position
        #    flag: One of EXACT, LOWER_BOUND, UPPER_BOUND
        if hash_key not in self.table:
            # New entry - check if table is full
            if len(self.table) >= self.max_size:
                self._replace_entry()
            
            self.table[hash_key] = {
                "depth": depth,
                "value": value,
                "flag": flag,
                "age": self.current_age
            }
        else:
            # Entry exists - only replace if we searched deeper
            existing_entry = self.table[hash_key]
            if depth > existing_entry["depth"]:
                existing_entry["depth"] = depth
                existing_entry["value"] = value
                existing_entry["flag"] = flag
                existing_entry["age"] = self.current_age
    
    def lookup(self, hash_key, depth, alpha=None, beta=None):
        # Args:
        #    hash_key: Zobrist hash from gamestate.BOARD_HASH
        #    depth: Current search depth
        #    alpha: Current alpha value (for pruning)
        #    beta: Current beta value (for pruning)
        # Returns:
        #    (value, flag) if a usable cached result is found, else None
        if hash_key not in self.table:
            return None
        
        entry = self.table[hash_key]
        
        # Only use cached result if we searched at least as deep
        if entry["depth"] < depth:
            return None
        
        value = entry["value"]
        flag = entry["flag"]
        
        # Check if the flag makes this result usable
        # This matters when used with alpha-beta pruning
        if flag == self.EXACT:
            return (value, flag)
        elif flag == self.LOWER_BOUND:
            # Value >= stored value
            if alpha is not None and value >= alpha:
                return (value, flag)
        elif flag == self.UPPER_BOUND:
            # Value <= stored value
            if beta is not None and value <= beta:
                return (value, flag)
        
        return None
    
    def clear(self):
        # Clear all entries from the transposition table
        self.table.clear()
        self.current_age = 0
    
    def increment_age(self):
        # Increment age counter for entries (call this each move)
        self.current_age += 1
    
    def _replace_entry(self):
        # Simple replacement strategy: remove the oldest entry with the lowest depth
        if not self.table:
            return
        
        # Find entry with minimum depth, then minimum age as tiebreaker
        worst_key = min(
            self.table.keys(),
            key=lambda k: (self.table[k]["depth"], self.table[k]["age"])
        )
        del self.table[worst_key]
    
    def get_size(self):
        # Return current number of entries in the table
        return len(self.table)
    
    def get_stats(self):
        # Return statistics about the transposition table
        if not self.table:
            return {
                "entries": 0,
                "avg_depth": 0,
                "max_depth": 0,
                "min_depth": 0,
                "exact_count": 0,
                "lower_bound_count": 0,
                "upper_bound_count": 0
            }
        
        depths = [entry["depth"] for entry in self.table.values()]
        flags = [entry["flag"] for entry in self.table.values()]
        
        return {
            "entries": len(self.table),
            "avg_depth": sum(depths) / len(depths),
            "max_depth": max(depths),
            "min_depth": min(depths),
            "exact_count": flags.count(self.EXACT),
            "lower_bound_count": flags.count(self.LOWER_BOUND),
            "upper_bound_count": flags.count(self.UPPER_BOUND)
        }

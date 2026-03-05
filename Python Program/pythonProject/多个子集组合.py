def find_subsets(numbers, target, num_subsets=20):
    from itertools import combinations
    from math import isclose
    # Since numbers are floats, we need to compare with tolerance
    tol = 1e-2
    # Convert target to float for consistency
    target = float(target)
    # We'll use indices to avoid duplicate subsets with same values but different indices
    indices = list(range(len(numbers)))
    # Sort numbers and indices together for pruning
    sorted_indices = sorted(indices, key=lambda i: numbers[i], reverse=True)
    sorted_numbers = [numbers[i] for i in sorted_indices]
    # Function to check sum with tolerance
    def is_target(s):
        return isclose(s, target, abs_tol=tol)
    found_subsets = []
    # Use DFS to find subsets
    def dfs(start, current_sum, current_indices):
        if len(found_subsets) >= num_subsets:
            return
        if is_target(current_sum):
            # Convert indices to original numbers
            subset = [numbers[i] for i in current_indices]
            found_subsets.append(subset)
            return
        if start >= len(sorted_indices):
            return
        if current_sum > target + tol:
            return  # Prune if exceeded
        # Include the current index
        new_sum = current_sum + sorted_numbers[start]
        new_indices = current_indices + [sorted_indices[start]]
        dfs(start+1, new_sum, new_indices)
        # Exclude the current index
        dfs(start+1, current_sum, current_indices)
    dfs(0, 0.0, [])
    return found_subsets

# Your numbers list
numbers = [275668.98, 102758.02, 81760, 5300, 9547.4, 37085.03, 13987.86, 977.8, 2005.76, 1424.86, 69246, 292851.51, 103305, 120260, 134000, 8565.25, 262961.94, 1563320.34, 37085.03, 13987.86, 977.8, 2005.76, 1424.86, 69246, 292851.51, 103305, 54152.06, 36591.81, 13664.11, 1937.23, 1986.88, 1392.48, 68962.8, 76000, 2600, 19334.5, 74702.94, 287284.84, 102009, 97578.21, 4500, 39096.97, 13664.11, 1937.23, 1986.88, 1392.48, 68962.8, 287284.84, 102009, 211622.2, 21755.76, 39376.95, 36342.69, 12881.2, 1806.7, 1853, 1288.22, 68962.8, 287284.84, 318129.18, 175477.38, 95541.6, 68962.8, 287284.84, 102009, 87360, 55187.4, 39096.97, 13923.7, 1937.23, 1986.88, 1392.48, 31125.45, 1295.65, 11703.05, 1170.4, 2053.49, 1642.78, 25150.9, 11210, 37000, 1440, 930, 930, 243682.18, 89946, 34414.38, 25519.2, 9724.55, 1830.83, 1343.78, 972.53, 50148.84, 94608, 4000, 206307.26, 300312, 38779.09, 30388.65, 10926.2, 2074.15, 1659.31, 1092.7, 1453.4, 45555.84, 18268.82, 197240.26, 74481, 44420, 29578.65, 10602.45, 2020.15, 1616.11, 1060.32, 1453.4, 45272.64, 3300, 39000, 191840.26, 258159.5, 54600.6, 29925.3, 10667.9, 2043.26, 1634.6, 1066.87, 1473.52, 45272.64, 16414.83, 340717.72, 192513.68, 82715, 24360, 30249.3, 10667.9, 2043.26, 1634.6, 1066.87, 1495.12, 52240.8, 1305.43, 22606.53, 52240.8, 240]

target = 7878866.91

# Find 10 subsets
subsets = find_subsets(numbers, target, 100)

# Output the subsets
for i, subset in enumerate(subsets):
    print(f"组合 {i+1}: {subset}")
    print(f"和: {sum(subset)} (目标: {target})")
    print()
#include "solver.h"
#include <queue>
#include <unordered_set>
#include <unordered_map>
#include <cmath>
#include <algorithm>
#include <functional>

// Hash function for Vec3 to use in unordered containers
namespace std {
    template<> struct hash<Vec3> {
        size_t operator()(const Vec3& v) const {
            return hash<int>()(v.x) ^ (hash<int>()(v.y) << 1) ^ (hash<int>()(v.z) << 2);
        }
    };
}

void SpatialSolver::load_grid(const std::vector<std::uint8_t>& grid_data, int w, int h, int d) {
    grid = grid_data;
    width = w;
    height = h;
    depth = d;
}

bool SpatialSolver::is_walkable(Vec3 pos) const {
    if (pos.x < 0 || pos.x >= width || pos.y < 0 || pos.y >= height || pos.z < 0 || pos.z >= depth) {
        return false;
    }
    size_t idx = static_cast<size_t>(pos.x) * height * depth + pos.y * depth + pos.z;
    return idx < grid.size() && grid[idx] == 0; // 0 = air, 1 = solid
}

int SpatialSolver::heuristic(Vec3 from, Vec3 to) const {
    // Manhattan distance - good for 3D grid pathfinding
    return std::abs(from.x - to.x) + std::abs(from.y - to.y) + std::abs(from.z - to.z);
}

// A* Node for priority queue
struct AStarNode {
    Vec3 pos;
    int g_cost;  // Cost from start
    int f_cost;  // g_cost + heuristic
    
    bool operator>(const AStarNode& other) const {
        return f_cost > other.f_cost;
    }
};

PathResult SpatialSolver::find_path(const PathRequest& request) {
    PathResult result;
    result.success = false;
    
    Vec3 start = request.start;
    Vec3 end = request.end;
    
    // Check if start and end are valid
    if (!is_walkable(start) && start != end) {
        // Start position is blocked, try positions around it
        // For redstone, we route on top of blocks
    }
    
    // Priority queue for A* (min-heap by f_cost)
    std::priority_queue<AStarNode, std::vector<AStarNode>, std::greater<AStarNode>> open_set;
    
    // Track visited nodes and their parents
    std::unordered_set<Vec3> closed_set;
    std::unordered_map<Vec3, Vec3> came_from;
    std::unordered_map<Vec3, int> g_scores;
    
    // Initialize with start node
    g_scores[start] = 0;
    open_set.push({start, 0, heuristic(start, end)});
    
    // 6-directional neighbors (cardinal + up/down)
    const int dx[] = {1, -1, 0, 0, 0, 0};
    const int dy[] = {0, 0, 1, -1, 0, 0};
    const int dz[] = {0, 0, 0, 0, 1, -1};
    
    while (!open_set.empty()) {
        AStarNode current = open_set.top();
        open_set.pop();
        
        // Skip if already processed
        if (closed_set.count(current.pos)) {
            continue;
        }
        
        // Goal reached!
        if (current.pos == end) {
            result.success = true;
            
            // Reconstruct path
            Vec3 curr = end;
            while (came_from.count(curr)) {
                result.path.push_back(curr);
                result.blocks.push_back("minecraft:redstone_wire");
                curr = came_from[curr];
            }
            result.path.push_back(start);
            result.blocks.push_back("minecraft:redstone_wire");
            
            // Reverse to get start-to-end order
            std::reverse(result.path.begin(), result.path.end());
            std::reverse(result.blocks.begin(), result.blocks.end());
            
            return result;
        }
        
        closed_set.insert(current.pos);
        
        // Explore neighbors
        for (int i = 0; i < 6; ++i) {
            Vec3 neighbor = {
                current.pos.x + dx[i],
                current.pos.y + dy[i],
                current.pos.z + dz[i]
            };
            
            // Skip if out of bounds or already visited
            if (closed_set.count(neighbor)) {
                continue;
            }
            
            // Check if walkable (or is the destination)
            if (!is_walkable(neighbor) && neighbor != end) {
                continue;
            }
            
            // Calculate cost (vertical movement costs more)
            int move_cost = 1;
            if (dy[i] != 0) {
                move_cost = 2;  // Vertical movement penalty
            }
            
            int tentative_g = current.g_cost + move_cost;
            
            // Check if this is a better path
            if (!g_scores.count(neighbor) || tentative_g < g_scores[neighbor]) {
                came_from[neighbor] = current.pos;
                g_scores[neighbor] = tentative_g;
                int f = tentative_g + heuristic(neighbor, end);
                open_set.push({neighbor, tentative_g, f});
            }
        }
    }
    
    // No path found
    return result;
}

bool SpatialSolver::check_qc_violation(Vec3 position, std::string block_type) {
    // Quasi-Connectivity (QC) affects pistons and droppers
    // A piston can be powered by blocks up to 2 blocks above its input
    
    if (block_type != "minecraft:piston" && block_type != "minecraft:sticky_piston") {
        return false;  // Only pistons have QC
    }
    
    // Check for unintended QC power sources within range
    const int QC_RANGE = 2;
    for (int dy = 1; dy <= QC_RANGE; ++dy) {
        Vec3 above = {position.x, position.y + dy, position.z};
        if (above.y < height) {
            size_t idx = static_cast<size_t>(above.x) * height * depth + above.y * depth + above.z;
            if (idx < grid.size() && grid[idx] == 1) {
                // There's a block above - could be QC issue
                // In a real implementation, check if it's a power source
                return true;  // Potential QC violation
            }
        }
    }
    
    return false;  // No violation
}

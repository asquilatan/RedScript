#include <vector>
#include <queue>
#include <unordered_set>
#include <cmath>
#include <limits>

struct Vec3Hash {
    std::size_t operator()(const Vec3& v) const {
        return std::hash<int>()(v.x) ^ (std::hash<int>()(v.y) << 1) ^ (std::hash<int>()(v.z) << 2);
    }
};

struct Node {
    Vec3 pos;
    int g_cost;  // Cost from start
    int h_cost;  // Heuristic to goal
    
    int f_cost() const { return g_cost + h_cost; }
    
    bool operator>(const Node& other) const {
        return f_cost() > other.f_cost();
    }
};

// Forward declarations
class SpatialSolver;

namespace Pathfinding {
    // Manhattan distance heuristic
    inline int heuristic(Vec3 from, Vec3 to) {
        return std::abs(from.x - to.x) + std::abs(from.y - to.y) + std::abs(from.z - to.z);
    }
    
    // Cost function for placing a redstone wire
    inline int wire_cost() { return 1; }
    
    // Cost function for placing a repeater
    inline int repeater_cost() { return 4; }  // Higher cost due to delay
    
    // Cost function for vertical transmission
    inline int vertical_cost() { return 3; }
}

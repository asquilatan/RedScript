#pragma once
#include <vector>
#include <string>
#include <unordered_map>
#include <cstdint>

struct Vec3 {
    int x, y, z;
    
    bool operator==(const Vec3& other) const {
        return x == other.x && y == other.y && z == other.z;
    }

    bool operator!=(const Vec3& other) const {
        return !(*this == other);
    }
};

struct PathRequest {
    Vec3 start;
    Vec3 end;
    int signal_strength;
    bool allow_vertical;
    int min_delay;
    int max_delay;
};

struct PathResult {
    bool success;
    std::vector<Vec3> path;
    std::vector<std::string> blocks; // e.g., "dust", "repeater"
};

class SpatialSolver {
private:
    std::vector<std::uint8_t> grid;
    int width, height, depth;
    
public:
    /**
     * Initializes the solver with the current grid state.
     * @param grid_data Serialized representation of occupied voxels.
     * @param width Grid width
     * @param height Grid height
     * @param depth Grid depth
     */
    void load_grid(const std::vector<std::uint8_t>& grid_data, int width, int height, int depth);

    /**
     * Finds a valid redstone path between two points using A*.
     * Handles signal strength decay and repeater insertion.
     */
    PathResult find_path(const PathRequest& request);

    /**
     * Checks if a proposed block placement violates quasi-connectivity rules.
     */
    bool check_qc_violation(Vec3 position, std::string block_type);
    
private:
    bool is_walkable(Vec3 pos) const;
    int heuristic(Vec3 from, Vec3 to) const;
};

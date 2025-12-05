#pragma once
#include <vector>
#include <string>

struct Vec3 {
    int x, y, z;
};

struct PathRequest {
    Vec3 start;
    Vec3 end;
    int signal_strength;
    bool allow_vertical;
};

struct PathResult {
    bool success;
    std::vector<Vec3> path;
    std::vector<std::string> blocks; // e.g., "dust", "repeater"
};

class SpatialSolver {
public:
    /**
     * Initializes the solver with the current grid state.
     * @param grid_data Serialized representation of occupied voxels.
     */
    void load_grid(const std::vector<uint8_t>& grid_data, int width, int height, int depth);

    /**
     * Finds a valid redstone path between two points using A*.
     * Handles signal strength decay and repeater insertion.
     */
    PathResult find_path(const PathRequest& request);

    /**
     * Checks if a proposed block placement violates quasi-connectivity rules.
     */
    bool check_qc_violation(Vec3 position, std::string block_type);
};

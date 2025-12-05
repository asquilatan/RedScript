#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "solver.h"

namespace py = pybind11;

PYBIND11_MODULE(_solver, m) {
    m.doc() = "RedScript C++ Solver Extension";

    // Bind Vec3 struct
    py::class_<Vec3>(m, "Vec3")
        .def(py::init<int, int, int>())
        .def_readwrite("x", &Vec3::x)
        .def_readwrite("y", &Vec3::y)
        .def_readwrite("z", &Vec3::z)
        .def("__repr__", [](const Vec3& v) {
            return "Vec3(" + std::to_string(v.x) + ", " + std::to_string(v.y) + ", " + std::to_string(v.z) + ")";
        });

    // Bind PathRequest struct
    py::class_<PathRequest>(m, "PathRequest")
        .def(py::init<>())
        .def_readwrite("start", &PathRequest::start)
        .def_readwrite("end", &PathRequest::end)
        .def_readwrite("signal_strength", &PathRequest::signal_strength)
        .def_readwrite("allow_vertical", &PathRequest::allow_vertical)
        .def_readwrite("min_delay", &PathRequest::min_delay)
        .def_readwrite("max_delay", &PathRequest::max_delay);

    // Bind PathResult struct
    py::class_<PathResult>(m, "PathResult")
        .def(py::init<>())
        .def_readwrite("success", &PathResult::success)
        .def_readwrite("path", &PathResult::path)
        .def_readwrite("blocks", &PathResult::blocks);

    // Bind SpatialSolver class
    py::class_<SpatialSolver>(m, "SpatialSolver")
        .def(py::init<>())
        .def("load_grid", &SpatialSolver::load_grid)
        .def("find_path", &SpatialSolver::find_path)
        .def("check_qc_violation", &SpatialSolver::check_qc_violation);
}

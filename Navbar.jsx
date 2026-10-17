import React, { useContext } from 'react';
import { Link, useNavigate } from "react-router-dom";
import { LoginContext } from "../App";
import sunbeamLogo from "../assets/sunbeam_LOGO.jpeg";

function Navbar() {
  const { loginstatus, setloginstatus, username, userrole } = useContext(LoginContext);
  const navigate = useNavigate();

  const logout = () => {
    setloginstatus(false);
    navigate("/home");
  };

  const changepassword = () => {
    navigate("/updatepassword");
  };

  return (
    <>
      {/* Top Navbar */}
      <nav className="navbar navbar-expand-lg" style={{ backgroundColor: '#00bcd4' }}>
        <div className="container-fluid">
          <Link className="navbar-brand text-white fw-bold d-flex align-items-center" to="/home">
            <img
              src={sunbeamLogo}
              alt="Sunbeam Logo"
              height="40"
              style={{ marginRight: "8px", borderRadius: "50%" }}
            />
            {loginstatus && userrole === 'admin' ? "STUDENT PORTAL" : "SUNBEAM INFOTECH"}
          </Link>

          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#topNavbar"
            aria-controls="topNavbar"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse" id="topNavbar">
            <ul className="navbar-nav me-auto">
              <li className="nav-item ms-3">
                <Link className="nav-link text-white" to="/home">Home</Link>
              </li>
              <li className="nav-item ms-3">
                <Link className="nav-link text-white" to="/aboutus">About</Link>
              </li>
              {loginstatus && userrole === 'student' && (
                <li className="nav-item ms-3">
                  <Link className="nav-link text-white" to="/mycourses">My Courses</Link>
                </li>
              )}
            </ul>

            <ul className="navbar-nav ms-auto">
              {!loginstatus ? (
                <li className="nav-item">
                  <Link
                    className="nav-link text-white fw-bold"
                    to="/login"
                    style={{ backgroundColor: "rgb(0, 43, 73)", borderRadius: '20%' }}
                  >
                    Login
                  </Link>
                </li>
              ) : (
                <li className="nav-item dropdown">
                  <span
                    className="nav-link dropdown-toggle text-white fw-bold border rounded px-2"
                    role="button"
                    data-bs-toggle="dropdown"
                    style={{ cursor: "pointer" }}
                  >
                    {username}
                  </span>
                  <ul className="dropdown-menu dropdown-menu-end">
                    <li>
                      <button className="dropdown-item" onClick={changepassword}>Update Password</button>
                    </li>
                    <li><hr className="dropdown-divider" /></li>
                    <li>
                      <button className="dropdown-item text-danger" onClick={logout}>Sign Out</button>
                    </li>
                  </ul>
                </li>
              )}
            </ul>
          </div>
        </div>
      </nav>

      {/* Admin Second Navbar */}
      {loginstatus && userrole === 'admin' && (
        <nav className="navbar navbar-expand-lg py-0" style={{ backgroundColor: '#0d6efd' }}>
          <div className="container-fluid justify-content-center">
            <ul className="navbar-nav flex-row">
              <li className="nav-item px-3">
                <Link className="nav-link text-white fw-bold" to="/dashboard">Dashboard</Link>
              </li>

              <li className="nav-item dropdown px-3">
                <span className="nav-link dropdown-toggle text-white fw-bold" role="button" data-bs-toggle="dropdown">
                  Courses
                </span>
                <ul className="dropdown-menu">
                  <li><Link className="dropdown-item" to="/addcourse">Add Course</Link></li>
                  <li><Link className="dropdown-item" to="/getallcoursess">Get All Courses</Link></li>
                  <li><Link className="dropdown-item" to="/updatecourses">Update Courses</Link></li>
                </ul>
              </li>

              <li className="nav-item dropdown px-3">
                <span className="nav-link dropdown-toggle text-white fw-bold" role="button" data-bs-toggle="dropdown">
                  Videos
                </span>
                <ul className="dropdown-menu">
                  <li><Link className="dropdown-item" to="/addvideos">Add Videos</Link></li>
                  <li><Link className="dropdown-item" to="/getallvideos">Get All Videos</Link></li>
                </ul>
              </li>

              <li className="nav-item dropdown px-3">
                <span className="nav-link dropdown-toggle text-white fw-bold" role="button" data-bs-toggle="dropdown">
                  Students
                </span>
                <ul className="dropdown-menu">
                  <li><Link className="dropdown-item" to="/getallstudents">Get All Students</Link></li>
                </ul>
              </li>
            </ul>
          </div>
        </nav>
      )}
    </>
  );
}

export default Navbar;

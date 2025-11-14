import { Link, useNavigate } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer";

export const Navbar = () => {
  const { store, dispatch } = useGlobalReducer();
  const navigate = useNavigate();

  const handleLogout = () => {
    sessionStorage.removeItem("token");
    dispatch({ type: "logout" });
    navigate("/login");
  };

  return (
    <nav className="navbar navbar-light bg-light mb-3">
      <div className="container">
        <Link to="/" className="navbar-brand mb-0 h1">
          React Flask Auth
        </Link>
        <div className="ml-auto">
          {store.token ? (
            <>
              <Link to="/private" className="btn btn-success me-2">
                Privado
              </Link>
              <button className="btn btn-outline-danger" onClick={handleLogout}>
                Cerrar sesión
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-primary me-2">
                Login
              </Link>
              <Link to="/signup" className="btn btn-outline-primary">
                Signup
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer";

export const Private = () => {
  const { store, dispatch } = useGlobalReducer();
  const navigate = useNavigate();
  const [message, setMessage] = useState(null);
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  useEffect(() => {
    const token = store.token || sessionStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    const load = async () => {
      const resp = await fetch(backendUrl + "/api/private", {
        headers: { Authorization: "Bearer " + token }
      });

      if (!resp.ok) {
        sessionStorage.removeItem("token");
        dispatch({ type: "logout" });
        navigate("/login");
        return;
      }

      const data = await resp.json();
      setMessage("Bienvenido " + data.user.email);
    };

    load();
  }, [store.token, backendUrl, navigate, dispatch]);

  return (
    <div className="container mt-5">
      <h2>Zona privada</h2>
      <p>{message || "Cargando..."}</p>
    </div>
  );
};
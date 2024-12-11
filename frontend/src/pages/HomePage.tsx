import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { isApiKeySet, setApiKey, validateApiKey } from "../apiKeyUtils.ts";
import ApiKeyInputField, {
  ApiKeyValidationStatus,
} from "../components/ApiKeyInputField.tsx";
import { useAuth } from "../authContext.tsx";

const DUMMY_API_KEY = "api-key";

function HomePage() {
  const [keyValidationStatus, setKeyValidationStatus] =
    useState<ApiKeyValidationStatus>("none");
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/login");
    }
  }, [isAuthenticated, navigate]);

  const onApiKeyValidationTrigger = (key: string) => {
    if (!key) {
      setKeyValidationStatus("none");
      return;
    }
    setKeyValidationStatus("validating");
    validateApiKey(key).then((isValid) => {
      setKeyValidationStatus(isValid ? "success" : "error");
      if (isValid) {
        setApiKey(key);
      }
    });
  };

  const isApiKeyValid = isApiKeySet();

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="d-flex flex-column min-vh-100">
      <div className="m-auto">
        <div className="d-flex justify-content-between mb-4">
          <button onClick={logout} className="btn btn-secondary">
            Logout
          </button>
        </div>
        <h1 className="text-center mb-4">JUMPI</h1>
        <div className="d-flex gap-2 flex-wrap justify-content-center">
          <Link
            to={isApiKeyValid ? "/search" : "#"}
            className={
              "btn btn-primary btn-lg mx-auto" +
              (isApiKeyValid ? "" : " disabled")
            }
          >
            Search
          </Link>
          <Link
            to={isApiKeyValid ? "/upload" : "#"}
            className={
              "btn btn-primary btn-lg mx-auto" +
              (isApiKeyValid ? "" : " disabled")
            }
          >
            Upload
          </Link>
        </div>
        <div className="mt-4">
          <label htmlFor="apiKey" className="form-label">
            API Key:
          </label>
          <ApiKeyInputField
            validationStatus={keyValidationStatus}
            onKeyUpdate={onApiKeyValidationTrigger}
            initialValue={(isApiKeySet() && DUMMY_API_KEY) || ""}
          />
        </div>
      </div>
    </div>
  );
}

export default HomePage;

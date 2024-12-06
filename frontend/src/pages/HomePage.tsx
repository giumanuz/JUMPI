import { Link } from "react-router-dom";
import { useState } from "react";
import axiosInstance from "../axiosInstance.ts";
import ApiKeyInputField, {
  ApiKeyValidationStatus,
} from "../components/ApiKeyInputField.tsx";

const DUMMY_API_KEY = "api-key";

function HomePage() {
  const [apiKey, setApiKey] = useState(
    (localStorage.getItem("apiKey") && DUMMY_API_KEY) ?? "",
  );
  const [keyValidationStatus, setKeyValidationStatus] =
    useState<ApiKeyValidationStatus>("none");

  const isApiKeyValid = () => {
    return (
      keyValidationStatus === "success" ||
      (keyValidationStatus === "none" && apiKey)
    );
  };

  const updateApiKey = (key: string) => {
    if (!key || key === DUMMY_API_KEY) {
      return;
    }
    setApiKey(key);
    localStorage.setItem("apiKey", key);
    axiosInstance.defaults.headers.common["X-API-KEY"] = key;
  };

  const onApiKeyValidationTrigger = (key: string) => {
    if (!key) {
      setKeyValidationStatus("none");
      return;
    }
    setKeyValidationStatus("validating");
    axiosInstance
      .get("/validate-api-key", { headers: { "X-API-KEY": key } })
      .then(() => {
        setKeyValidationStatus("success");
        updateApiKey(key);
      })
      .catch(() => {
        setKeyValidationStatus("error");
      });
  };

  return (
    <div className="d-flex flex-column min-vh-100">
      <div className="m-auto">
        <h1 className="text-center mb-4">JUMPI</h1>
        <div className="d-flex gap-2">
          <Link
            to={isApiKeyValid() ? "/search" : "#"}
            className={
              "btn btn-primary btn-lg mx-auto" +
              (isApiKeyValid() ? "" : " disabled")
            }
          >
            Search
          </Link>
          <Link
            to={isApiKeyValid() ? "/upload" : "#"}
            className={
              "btn btn-primary btn-lg mx-auto" +
              (isApiKeyValid() ? "" : " disabled")
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
            initialValue={apiKey}
          />
        </div>
      </div>
    </div>
  );
}

export default HomePage;

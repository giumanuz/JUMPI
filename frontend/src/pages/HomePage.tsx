import { useState } from "react";
import { Link } from "react-router-dom";
import { isApiKeySet, setApiKey, validateApiKey } from "../apiKeyUtils.ts";
import ApiKeyInputField, {
  ApiKeyValidationStatus,
} from "../components/ApiKeyInputField.tsx";

const DUMMY_API_KEY = "api-key";

function HomePage() {
  const [keyValidationStatus, setKeyValidationStatus] =
    useState<ApiKeyValidationStatus>("none");

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

  return (
    <div className="d-flex flex-column min-vh-100">
      <div className="m-auto">
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

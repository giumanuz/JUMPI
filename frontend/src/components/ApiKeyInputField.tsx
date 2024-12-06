import React, { useEffect, useState } from "react";
import { FaCheckCircle, FaTimesCircle } from "react-icons/fa";

export type ApiKeyValidationStatus =
  | "none"
  | "validating"
  | "success"
  | "error";

type ApiKeyInputFieldProps = {
  initialValue: string;
  validationStatus: ApiKeyValidationStatus;
  onKeyUpdate: (key: string) => void;
};

export function ApiKeyInputField({
  initialValue,
  validationStatus,
  onKeyUpdate,
}: ApiKeyInputFieldProps) {
  const [text, setText] = useState(initialValue || "");
  const [inputTimeoutId, setInputTimeoutId] = useState<number>();

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newKey = event.target.value;
    setText(newKey);
    if (inputTimeoutId) {
      clearTimeout(inputTimeoutId);
    }
    const timeout = setTimeout(() => {
      console.log("ciao");
      onKeyUpdate(newKey);
    }, 600);
    setInputTimeoutId(timeout);
  };

  useEffect(() => {
    // Clean up timeout on unmount
    return () => {
      if (inputTimeoutId) {
        clearTimeout(inputTimeoutId);
      }
    };
  }, [inputTimeoutId]);

  return (
    <div className="d-flex align-items-center">
      <input
        type="password"
        className="form-control"
        value={text}
        onChange={handleInputChange}
        placeholder="Enter your API key"
      />
      <div className="ms-2 d-flex align-items-center">
        {validationStatus === "validating" && <Spinner />}
        {validationStatus === "success" && (
          <FaCheckCircle className={"text-success"} size="1.5rem" />
        )}
        {validationStatus === "error" && (
          <FaTimesCircle className={"text-danger"} size="1.5rem" />
        )}
      </div>
    </div>
  );
}

function Spinner() {
  return (
    <div
      className="spinner-border text-primary spinner-border-sm"
      role="status"
    >
      <span className="visually-hidden">Loading...</span>
    </div>
  );
}

export default ApiKeyInputField;

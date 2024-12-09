import { FormEventHandler, ReactNode } from "react";
import "../styles/FormTemplate.scss";

type FormTemplateProps = {
  title: string;
  children: ReactNode[];
  button: ReactNode;
  loading?: boolean;
  loadingDescription?: string;
  onSubmit: FormEventHandler<HTMLFormElement>;
  columns?: number;
  preFormContent?: ReactNode;
};

const FormTemplate = ({
  children,
  button,
  loading,
  loadingDescription,
  title,
  onSubmit,
  columns,
  preFormContent,
}: FormTemplateProps) => (
  <div className="d-flex justify-content-center align-items-center vh-100">
    <div
      className="card bg-body-secondary p-4 shadow-sm"
      style={{ width: "50rem" }}
    >
      <h3 className="text-center mb-4">{title}</h3>
      <form onSubmit={onSubmit}>
        {preFormContent && <div className="mb-3">{preFormContent}</div>}
        <div className="container">{children}</div>
        <div className="d-flex justify-content-end mt-4">{button}</div>
      </form>

      {loading && (
        <div className="text-center mt-3">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p>{loadingDescription || "Processing..."}</p>
        </div>
      )}
    </div>
  </div>
);

export default FormTemplate;

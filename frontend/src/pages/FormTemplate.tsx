import {FormEvent, ReactNode} from 'react';

type FormTemplateProps = {
  title: string;
  children: ReactNode;
  button: HTMLButtonElement;
  loading?: boolean;
  loadingDescription?: string;
  onSubmit: FormEvent<HTMLFormElement>;
}

const FormTemplate = ({children, button, loading, loadingDescription, title, onSubmit}: FormTemplateProps) => (
  <div className="d-flex justify-content-center align-items-center vh-100">
    <div className="card bg-body-secondary p-4 shadow-sm" style={{width: '50rem'}}>
      <h3 className="text-center mb-4">{title}</h3>
      <form onSubmit={onSubmit}>
        <div className="row row-cols-2">
          {
            children.map((child, index) => (
              <div className="col" key={index}>
                {child}
              </div>
            ))
          }
        </div>
        {button}
      </form>

      {loading && (
        <div className="text-center mt-3">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p>{loadingDescription || ""}</p>
        </div>
      )}
    </div>
  </div>
);

export default FormTemplate;

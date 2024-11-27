import { ChangeEvent } from 'react';

interface InputFieldProps {
  id: string;
  label: string;
  placeholder: string;
  value: string;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
  type?: string;
}

const InputField: React.FC<InputFieldProps> = ({ id, label, placeholder, value, onChange, type = 'text' }) => (
  <div className="mb-3">
    <label htmlFor={id} className="form-label">
      {label}
    </label>
    <input
      type={type}
      className="form-control"
      id={id}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
    />
  </div>
);

export default InputField;

import { ChangeEvent, FC } from "react";

export type InputFieldProps = {
  id?: string;
  label: string;
  placeholder?: string;
  value: string;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
  type?: string;
  required?: boolean;
};

const InputField: FC<InputFieldProps> = ({
  label,
  value,
  onChange,
  id = label,
  type = "text",
  placeholder = "",
  required = false,
}) => (
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
      required={required}
    />
  </div>
);

export default InputField;

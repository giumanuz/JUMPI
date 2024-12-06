import { ChangeEvent, FC } from "react";

export type TextAreaFieldProps = {
  id: string;
  label: string;
  placeholder: string;
  value: string;
  onChange: (e: ChangeEvent<HTMLTextAreaElement>) => void;
  rows?: number;
  required?: boolean;
};

const TextAreaField: FC<TextAreaFieldProps> = ({
  id,
  label,
  placeholder,
  value,
  onChange,
  rows = 3,
  required = false,
}) => (
  <div className="mb-3">
    <label htmlFor={id} className="form-label">
      {label}
    </label>
    <textarea
      className="form-control"
      id={id}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      rows={rows}
      required={required}
    ></textarea>
  </div>
);

export default TextAreaField;

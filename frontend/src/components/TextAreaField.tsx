import {ChangeEvent, FC} from 'react';

type TextAreaFieldProps = {
  id: string;
  label: string;
  placeholder: string;
  value: string;
  onChange: (e: ChangeEvent<HTMLTextAreaElement>) => void;
  rows?: number;
}

const TextAreaField: FC<TextAreaFieldProps> = ({id, label, placeholder, value, onChange, rows = 3}) => (
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
    ></textarea>
  </div>
);

export default TextAreaField;

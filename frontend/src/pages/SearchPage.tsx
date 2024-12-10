import { ChangeEvent, FormEvent, useState } from "react";
import InputField from "../components/InputField";
import TextAreaField from "../components/TextAreaField";
import FormTemplate from "./FormTemplate.tsx";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance.ts";
import { AxiosError } from "axios";

const SearchPage = () => {
  const [params, setParams] = useState({
    magazine_name: "",
    magazine_date: "",
    magazine_publisher: "",
    magazine_genre: "",
    article_title: "",
    article_author: "",
    article_content: "",
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setParams((prevData) => ({
      ...prevData,
      [id]: value,
    }));
  };

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axiosInstance.get(`/query`, { params });
      navigate("/queryResults", { state: { results: response.data } });
      console.log(response);
    } catch (error) {
      const axiosError = error as AxiosError;
      console.error("Error uploading documents:", error);
      const data = axiosError?.response?.data as { error?: string };
      const text = data?.error || "An unexpected error occurred.";
      console.error("Error querying:", error);
      alert(`Failed to execute query: ${text}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <FormTemplate
      title={"Search for an article"}
      loading={loading}
      button={
        <button type="submit" className="btn btn-primary w-100">
          Search
        </button>
      }
      onSubmit={onSubmit}
    >
      <InputField
        id="magazine_name"
        label="Magazine Name"
        placeholder="Enter magazine name"
        value={params.magazine_name}
        onChange={onChange}
      />
      <InputField
        id="magazine_date"
        label="Date"
        placeholder="Enter date of publication"
        value={params.magazine_date}
        onChange={onChange}
        type="string"
      />
      <InputField
        id="magazine_publisher"
        label="Magazine Publisher"
        placeholder="Enter magazine publisher's name"
        value={params.magazine_publisher}
        onChange={onChange}
      />
      <InputField
        id="magazine_genre"
        label="Magazine Genre"
        placeholder="Enter genre (e.g., Science)"
        value={params.magazine_genre}
        onChange={onChange}
      />
      <InputField
        id="article_title"
        label="Article Title"
        placeholder="Enter article title"
        value={params.article_title}
        onChange={onChange}
      />
      <InputField
        id="article_author"
        label="Article Author"
        placeholder="Enter author's name"
        value={params.article_author}
        onChange={onChange}
      />
      <TextAreaField
        id="article_content"
        label="Article Content"
        placeholder="Enter article content"
        value={params.article_content}
        onChange={onChange}
      />
    </FormTemplate>
  );
};

export default SearchPage;

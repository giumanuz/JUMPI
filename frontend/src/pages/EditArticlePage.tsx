import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import FormTemplate from "../pages/FormTemplate";

interface Article {
  id: string;
  magazine_id: string;
  title: string;
  author: string;
  page_range: number[];
  content: string;
  page_offsets: number[];
  figures: any[]; // Definisci correttamente secondo necessità
  created_on: string;
  edited_on: string;
}

function EditArticlePage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [article, setArticle] = useState<Article | null>(null);
  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [pageRange, setPageRange] = useState("");
  const [content, setContent] = useState("");
  // Aggiungi altri campi se necessario
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      axiosInstance
        .get(`/articles/${id}`)
        .then((res) => {
          setArticle(res.data.article);
          setTitle(res.data.article.title);
          setAuthor(res.data.article.author);
          setPageRange(res.data.article.page_range.join("-"));
          setContent(res.data.article.content);
          // Inizializza altri campi se necessario
        })
        .catch((err) => {
          console.error("Errore nel recupero dell'articolo:", err);
          setError("Errore nel recupero dell'articolo.");
        });
    }
  }, [id]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!id) {
      setError("ID dell'articolo mancante.");
      return;
    }

    const pageRangeRegex = /^\d+-\d+$/;
    if (!pageRangeRegex.test(pageRange)) {
      setError('Page Range deve essere nel formato "start-end", es. "1-5".');
      return;
    }

    const updatedArticle = {
      title,
      author,
      page_range: pageRange.split("-").map(Number),
      content,
      // Includi altri campi se necessario
    };

    try {
      const res = await axiosInstance.put(`/articles/${id}`, updatedArticle);

      if (res.status === 200) {
        setSuccessMessage("Articolo aggiornato con successo!");
        setTimeout(() => {
          navigate(`/manageArticles/${article?.magazine_id}`);
        }, 2000);
      } else {
        setError("Errore nell'aggiornamento dell'articolo.");
      }
    } catch (err) {
      console.error("Errore nell'aggiornamento dell'articolo:", err);
      setError("Errore nell'aggiornamento dell'articolo.");
    }
  };

  if (!article) {
    return <div className="container mt-4">Caricamento...</div>;
  }

  return (
    <FormTemplate
      title="Modifica Articolo"
      onSubmit={handleSubmit}
      button={
        <button type="submit" className="btn btn-primary mt-3">
          Salva Modifiche
        </button>
      }
    >
      {error && <div className="alert alert-danger">{error}</div>}
      {successMessage && (
        <div className="alert alert-success">{successMessage}</div>
      )}
      <div className="mb-3">
        <label className="form-label">Titolo</label>
        <input
          type="text"
          className="form-control"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Autore</label>
        <input
          type="text"
          className="form-control"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Page Range (es. "1-5")</label>
        <input
          type="text"
          className="form-control"
          value={pageRange}
          onChange={(e) => setPageRange(e.target.value)}
          placeholder="es. 1-5"
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Contenuto</label>
        <textarea
          className="form-control"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={5}
        ></textarea>
      </div>
      {/* Aggiungi altri campi se necessario */}
    </FormTemplate>
  );
}

export default EditArticlePage;

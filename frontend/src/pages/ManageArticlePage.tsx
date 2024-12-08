import { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";
import { useLocation, useNavigate } from "react-router-dom";
import ArticleCard from "../components/ArticleCard";

interface Article {
  id: string;
  magazine_id: string;
  title: string;
  author: string;
  page_range: number[];
  content: string;
  page_offsets: number[];
  figures: any[];
  created_on: string;
  edited_on: string;
}

interface Magazine {
  id: string;
  name: string;
  date: string;
  publisher: string;
  edition?: string;
  abstract?: string;
  genres?: string[];
  categories?: string[];
}

function ManageArticlePage() {
  const { search } = useLocation();
  const queryParams = new URLSearchParams(search);
  const magazineId = queryParams.get("magazine_id");
  const navigate = useNavigate();
  const [articles, setArticles] = useState<Article[]>([]);
  const [magazine, setMagazine] = useState<Magazine | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (magazineId) {
      // I know that this api call could be avoided by passing the magazine data from the previous page, but from now on I will keep it like this
      axiosInstance
        .get(`/magazineInfo?id=${magazineId}`)
        .then((res) => {
          console.log(res.data.magazine);
          setMagazine(res.data.magazine);
        })
        .catch((err) => {
          console.error("Error retrieving the magazine:", err);
          setError("Error retrieving the magazine.");
        });

      axiosInstance
        .get(`/getArticlesFromMagazineid=${magazineId}`)
        .then((res) => {
          // TODO: IMPLEMNET getArticlesFromMagazineid in backend
          setArticles(res.data.articles);
        })
        .catch((err) => {
          console.error("Error retrieving articles:", err);
          setError("Error retrieving articles.");
        });
    }
  }, [magazineId]);

  if (!magazine) {
    return <div className="container mt-4">Loading magazine data...</div>;
  }

  return (
    <div className="container mt-4">
      <h1>Manage Articles</h1>
      <h3>Magazine: {magazine.name}</h3>
      {error && <div className="alert alert-danger">{error}</div>}
      <div className="row">
        {articles.length > 0 ? (
          articles.map((article) => {
            const dataForCard = {
              _id: magazine.id,
              name: magazine.name,
              year: magazine.date.substring(0, 4),
              publisher: magazine.publisher,
              genre:
                magazine.genres && magazine.genres.length > 0
                  ? magazine.genres[0]
                  : "N/A",
              articles: [article],
            };

            return (
              <div className="col-4 mb-3" key={article.id}>
                <ArticleCard
                  data={dataForCard}
                  onEdit={() =>
                    navigate(`/editArticle/${article.id}`, {
                      state: { data: dataForCard },
                    })
                  }
                />
              </div>
            );
          })
        ) : (
          <p>No articles found for this magazine.</p>
        )}
      </div>
    </div>
  );
}

export default ManageArticlePage;

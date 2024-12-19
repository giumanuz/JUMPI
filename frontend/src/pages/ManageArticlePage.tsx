import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import ArticleCard from "../components/ArticleCard";
import { getArticles, getMagazineFromId } from "../webApi";

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
      // TODO: Pass magazine through location state
      getMagazineFromId(magazineId).then(setMagazine);
      getArticles(magazineId).then(setArticles);
    }
  }, [magazineId]);

  if (!magazine) {
    return <div className="container mt-4">Loading magazine data...</div>;
  }

  console.log(articles);

  return (
    <div className="container mt-4">
      <h1>Manage Articles</h1>
      <h3>Magazine: {magazine.name}</h3>
      {error && <div className="alert alert-danger">{error}</div>}
      <div className="row">
        {articles.length > 0 ? (
          articles.map((article) => (
            <div className="col-4 mb-3" key={article.id}>
              <ArticleCard
                article={article}
                onEdit={() =>
                  navigate(`/editArticle?id=${article.id}`, {
                    state: { article },
                  })
                }
              />
            </div>
          ))
        ) : (
          <p>No articles found for this magazine.</p>
        )}
      </div>
    </div>
  );
}

export default ManageArticlePage;

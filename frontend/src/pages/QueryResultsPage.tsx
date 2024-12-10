import { useLocation } from "react-router-dom";
import ArticleCard from "../components/ArticleCard";

const QueryResultPage = () => {
  const location = useLocation();
  const results = location.state?.results ?? [];

  console.log("Query Results:", results);

  return (
    <div className="container mt-4">
      <h1>Search Results</h1>
      {results.length === 0 ? (
        <p>No results found.</p>
      ) : (
        <div className="row">
          {results.map((result: Article) => (
            <div className="col-md-4 mb-3" key={result.id}>
              <ArticleCard
                article={{
                  id: result.id,
                  title: result.title ?? "Untitled",
                  author: result.author ?? "Unknown",
                  content: result.content ?? "No content available.",
                  createdOn: new Date(result.createdOn || Date.now()),
                }}
                onEdit={() => {}}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default QueryResultPage;

import axiosInstance from "./axiosInstance";

export async function getMagazines(): Promise<Magazine[]> {
  const res = await axiosInstance.get("/getMagazines");
  return res.data.magazines.map((m: Magazine) => ({
    ...m,
    createdOn: new Date(m.createdOn),
    editedOn: new Date(m.editedOn),
    date: new Date(m.date),
  }));
}

export async function getMagazineFromId(id: string): Promise<Magazine> {
  const res = await axiosInstance.get(`/magazineInfo?id=${id}`);
  const magazine = res.data;
  console.log("magazine", magazine);
  magazine.createdOn = new Date(magazine.createdOn);
  magazine.editedOn = new Date(magazine.editedOn);
  magazine.date = new Date(magazine.date);
  return magazine;
}

export async function getArticleInfo(id: string): Promise<Article> {
  const res = await axiosInstance.get(`/articleInfo?id=${id}`);
  return res.data;
}

export async function getArticles(magazineId: string): Promise<Article[]> {
  const res = await axiosInstance.get(
    `/getArticlesFromMagazineid?id=${magazineId}`
  );
  return res.data.articles.map((a: Article) => ({
    ...a,
    createdOn: new Date(a.createdOn),
    editedOn: new Date(a.editedOn),
  }));
}

type UploadArticleRequiredKeys =
  | "title"
  | "author"
  | "pageRange"
  | "magazineId";
export async function uploadArticleAndGetResults(
  article: Pick<Article, UploadArticleRequiredKeys>,
  scans: FileList
): Promise<ArticleUploadResult> {
  console.log("pageRange", article.pageRange.join("-"));
  const formData = new FormData();
  formData.append("title", article.title);
  formData.append("author", article.author);
  formData.append("pageRange", article.pageRange.join("-"));
  formData.append("magazineId", article.magazineId);

  if (scans.length > 0) {
    Array.from(scans).forEach((scan, i) => {
      formData.append("scans", scan);
    });
  }

  return await axiosInstance.post("/uploadArticle", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

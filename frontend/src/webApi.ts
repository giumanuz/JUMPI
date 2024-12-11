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

export type UploadArticleRequiredKeys =
  | "title"
  | "author"
  | "pageRange"
  | "magazineId";

export async function uploadArticleAndGetResults(
  article: Pick<Article, UploadArticleRequiredKeys>,
  scans: FileList
): Promise<ArticleUploadResult> {
  try {
    const formData = new FormData();
    formData.append("title", article.title);
    formData.append("author", article.author);
    //  La libreria FormData non supporta direttamente la serializzazione di array o oggetti complessi, quindi si deve convertire pageRange in un JSON string e poi fare il parsing lato server (oppure direttamente parsare lato backend)
    formData.append("pageRange", JSON.stringify(article.pageRange));
    formData.append("magazineId", article.magazineId);

    if (scans && scans.length > 0) {
      Array.from(scans).forEach((scan) => {
        console.log(scan);
        formData.append("scans", scan);
      });
    }

    const response = await axiosInstance.post("/uploadArticle", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    if (response.status === 200 && response.data) {
      const result = response.data;

      if (!result.scanResults) {
        throw new Error("The API response does not contain scanResults.");
      }

      return result;
    } else {
      throw new Error(`Unexpected API response: ${response.status}`);
    }
  } catch (error) {
    console.error("Error uploading article:", error);
    throw new Error("Failed to upload the article. Please try again.");
  }
}

function handleErrorResponse(error: any, defaultMessage: string): never {
  if (error.response) {
    const status = error.response.status;

    const errorMessages: Record<number, string> = {
      404: "User not found.",
      401: "Invalid credentials.",
      409: "User already exists.",
    };

    const message = errorMessages[status] || defaultMessage;
    throw new Error(message);
  }

  throw new Error(defaultMessage);
}

export async function handleLogin(
  email: string,
  password: string
): Promise<void> {
  try {
    const response = await axiosInstance.post("/login", {
      email,
      password,
    });

    if (response.status !== 200) {
      throw new Error("Error during login.");
    }
  } catch (error) {
    handleErrorResponse(error, "Failed to log in. Please try again.");
  }
}

export async function registerUser(
  username: string,
  email: string,
  password: string
): Promise<void> {
  try {
    const response = await axiosInstance.post("/register", {
      username,
      email,
      password,
    });

    if (response.status !== 200) {
      throw new Error("Error during registration.");
    }
  } catch (error) {
    handleErrorResponse(error, "Failed to register. Please try again.");
  }
}

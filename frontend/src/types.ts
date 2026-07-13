export type User = {
  id: number,
  username: string,
  first_name: string,
  last_name: string,
  profile: {
    id: number,
    avatar: string | null,
    birth_date: string | null,
    bio: string | null,
  },
  settings: {
    id: number,
    theme: "light" | "dark",
  },
  followers_count: number,
  following_count: number,
  is_verified: boolean,
}

-- SupabaseのSQL Editorで実行してください

CREATE TABLE posts (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at timestamp with time zone DEFAULT now(),
  username text NOT NULL,
  shoot_date date NOT NULL,
  prefecture text NOT NULL,
  place text NOT NULL,
  costume text NOT NULL,
  detail text NOT NULL
);

-- インデックス作成（検索高速化）
CREATE INDEX idx_shoot_date ON posts(shoot_date);
CREATE INDEX idx_prefecture ON posts(prefecture);
CREATE INDEX idx_costume ON posts(costume);

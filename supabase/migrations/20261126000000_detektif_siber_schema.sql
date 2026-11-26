-- Skema Database Supabase untuk Detektif Siber
-- Project ID: dgpnfsdvypvgfnddpfel (https://dgpnfsdvypvgfnddpfel.supabase.co)

CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

-- 1. Tabel Materi Buku Panduan (ED)
CREATE TABLE IF NOT EXISTS public.game_lessons (
  key TEXT PRIMARY KEY,
  sort_order INTEGER NOT NULL DEFAULT 0,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  tip TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2. Tabel Level / Kasus Investigasi (LV)
CREATE TABLE IF NOT EXISTS public.game_levels (
  level_index INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  difficulty TEXT NOT NULL,
  teaser TEXT NOT NULL DEFAULT '',
  lesson_keys JSONB NOT NULL DEFAULT '[]'::jsonb,
  terminal_vals JSONB NOT NULL DEFAULT '[]'::jsonb,
  story JSONB NOT NULL DEFAULT '[]'::jsonb,
  db_tables JSONB NOT NULL DEFAULT '{}'::jsonb,
  tasks JSONB NOT NULL DEFAULT '[]'::jsonb,
  web_pages JSONB NOT NULL DEFAULT '[]'::jsonb,
  scene_data JSONB,
  cctv_data JSONB,
  culprit JSONB NOT NULL DEFAULT '[]'::jsonb,
  ending_text TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3. Tabel Konfigurasi Visual / Wallpaper (WALL)
CREATE TABLE IF NOT EXISTS public.game_config (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 4. Tabel Profil & Progres Pemain (terhubung dengan Supabase Auth user metadata username)
CREATE TABLE IF NOT EXISTS public.player_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username TEXT NOT NULL,
  username_lower TEXT GENERATED ALWAYS AS (lower(trim(username))) STORED UNIQUE,
  xp INTEGER NOT NULL DEFAULT 0 CHECK (xp >= 0),
  avatar INTEGER NOT NULL DEFAULT 0,
  language TEXT NOT NULL DEFAULT 'id' CHECK (language IN ('id', 'en')),
  music BOOLEAN NOT NULL DEFAULT true,
  sound BOOLEAN NOT NULL DEFAULT true,
  seen BOOLEAN NOT NULL DEFAULT false,
  query_runs INTEGER NOT NULL DEFAULT 0 CHECK (query_runs >= 0),
  done JSONB NOT NULL DEFAULT '[]'::jsonb,
  progress JSONB NOT NULL DEFAULT '[]'::jsonb,
  read_lessons JSONB NOT NULL DEFAULT '{}'::jsonb,
  got_evidence JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_player_profiles_xp ON public.player_profiles (xp DESC);

CREATE TRIGGER trg_game_lessons_updated_at
  BEFORE UPDATE ON public.game_lessons
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_game_levels_updated_at
  BEFORE UPDATE ON public.game_levels
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_game_config_updated_at
  BEFORE UPDATE ON public.game_config
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_player_profiles_updated_at
  BEFORE UPDATE ON public.player_profiles
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

ALTER TABLE public.game_lessons ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.game_levels ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.game_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.player_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read game_lessons"
  ON public.game_lessons FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Public read game_levels"
  ON public.game_levels FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Public read game_config"
  ON public.game_config FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Public read player_profiles"
  ON public.player_profiles FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Public insert player_profiles"
  ON public.player_profiles FOR INSERT
  TO anon, authenticated
  WITH CHECK (length(trim(username)) > 0);

CREATE POLICY "Public update player_profiles"
  ON public.player_profiles FOR UPDATE
  TO anon, authenticated
  USING (true)
  WITH CHECK (length(trim(username)) > 0);

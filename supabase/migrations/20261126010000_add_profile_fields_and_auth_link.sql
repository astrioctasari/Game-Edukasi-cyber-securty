-- Tambahan kolom profil pemain & tautan ke auth.users untuk fitur Edit Profil & Login OTP
ALTER TABLE public.player_profiles
  ADD COLUMN IF NOT EXISTS user_id UUID UNIQUE REFERENCES auth.users(id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS email TEXT NOT NULL DEFAULT '',
  ADD COLUMN IF NOT EXISTS display_name TEXT NOT NULL DEFAULT '',
  ADD COLUMN IF NOT EXISTS bio TEXT NOT NULL DEFAULT '';

CREATE INDEX IF NOT EXISTS idx_player_profiles_email_lower
  ON public.player_profiles (lower(email));

UPDATE public.player_profiles p
SET
  user_id = u.id,
  email = COALESCE(u.email, p.email)
FROM auth.users u
WHERE p.user_id IS NULL
  AND lower(COALESCE(u.raw_user_meta_data->>'username', '')) = p.username_lower;

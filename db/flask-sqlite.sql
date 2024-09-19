create table if not exists usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
);

create table if not exists exercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL,
    usuario INTEGER NOT NULL
);

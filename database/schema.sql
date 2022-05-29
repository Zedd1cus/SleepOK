CREATE TABLE IF NOT EXISTS users (
    TID BIGINT PRIMARY KEY , -- ид из телеграмма
    TimeToUP TIME, -- время подъема
    TimeToSleep TIME, -- время засыпания
    NotificationTime TIME[] DEFAULT '{}', -- массив времен для уведомлений

    Node INT DEFAULT 0, -- узел обработки, на котором находится пользователь
    CreatedDate TIMESTAMP DEFAULT NOW() -- дата регистрации
);

-- оценки ощущения пользователя
CREATE TABLE IF NOT EXISTS marks (
    UID SERIAL,
    TID INT , -- ид пользователя
    Value INT , -- оценка его состояния
    Timestamp TIMESTAMP DEFAULT NOW() -- время оценки
);
CREATE INDEX IF NOT EXISTS marks_tid ON marks(TID);
CREATE INDEX IF NOT EXISTS marks_uid ON marks(UID);


-- время подъема/засыпания пользователя
CREATE TABLE IF NOT EXISTS state_changes (
    UID SERIAL,
    TID INT, -- ид пользователя
    State INT , -- статус пользователя (0/1, лег/встал)
    Timestamp TIMESTAMP DEFAULT NOW() -- время изменения
);
CREATE INDEX IF NOT EXISTS state_changes_tid ON state_changes(TID);
CREATE INDEX IF NOT EXISTS state_changes_uid ON state_changes(UID);

-- советы для каждой оценки
CREATE TABLE IF NOT EXISTS advices (
    UID SERIAL PRIMARY KEY ,
    Marks INT[] DEFAULT '{}', -- настроение 1-5
    Hours INT[] DEFAULT '{}',
    Advice TEXT -- текст совета
);
CREATE INDEX IF NOT EXISTS advices_uid ON advices(UID);
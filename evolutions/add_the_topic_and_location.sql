ALTER TABLE presentations ADD COLUMN "topic_id" integer NULL REFERENCES "presentation_topics" ("id");
ALTER TABLE presentations ADD COLUMN "place_id" integer NULL REFERENCES "places" ("id");
CREATE INDEX "presentations_topic_id" ON "presentations" ("topic_id");
CREATE INDEX "presentations_place_id" ON "presentations" ("place_id");

-- Name: cache_container__created__idx; Type: INDEX; Schema: public; Owner: cms
CREATE INDEX IF NOT EXISTS cache_container__created__idx ON public.cache_container USING btree (created);
-- Name: cache_container__expire__idx; Type: INDEX; Schema: public; Owner: cms
CREATE INDEX IF NOT EXISTS cache_container__expire__idx ON public.cache_container USING btree (expire);
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
-- Name: panoramas_mission_name_585dc809_like; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_mission_name_585dc809_like ON public.panoramas_mission USING btree (name text_pattern_ops);
-- Name: panoramas_panorama__geolocation_2d_id; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_panorama__geolocation_2d_id ON public.panoramas_panorama USING gist (_geolocation_2d);
-- Name: panoramas_panorama__geolocation_2d_rd_id; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_panorama__geolocation_2d_rd_id ON public.panoramas_panorama USING gist (_geolocation_2d_rd);
-- Name: panoramas_panorama_geolocation_id; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_panorama_geolocation_id ON public.panoramas_panorama USING gist (geolocation extensions.gist_geometry_ops_nd);
-- Name: panoramas_panorama_mission_distance_23380198; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_panorama_mission_distance_23380198 ON public.panoramas_panorama USING btree (mission_distance);
-- Name: panoramas_panorama_mission_type_892c0f4b; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_panorama_mission_type_892c0f4b ON public.panoramas_panorama USING btree (mission_type);
-- Name: panoramas_panorama_mission_type_892c0f4b_like; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_panorama_mission_type_892c0f4b_like ON public.panoramas_panorama USING btree (mission_type text_pattern_ops);
-- Name: panoramas_panorama_mission_year_d5c2fa86; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_panorama_mission_year_d5c2fa86 ON public.panoramas_panorama USING btree (mission_year);
-- Name: panoramas_panorama_pano_id_868133f0_like; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_panorama_pano_id_868133f0_like ON public.panoramas_panorama USING btree (pano_id varchar_pattern_ops);
-- Name: panoramas_panorama_surface_type_3fb8aa73; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_panorama_surface_type_3fb8aa73 ON public.panoramas_panorama USING btree (surface_type);
-- Name: panoramas_panorama_surface_type_3fb8aa73_like; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_panorama_surface_type_3fb8aa73_like ON public.panoramas_panorama USING btree (surface_type varchar_pattern_ops);
-- Name: panoramas_panorama_tags_af7df1cc; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_panorama_tags_af7df1cc ON public.panoramas_panorama USING btree (tags);
-- Name: panoramas_region_pano_id_1d87b717; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_region_pano_id_1d87b717 ON public.panoramas_region USING btree (pano_id);
-- Name: panoramas_region_pano_id_1d87b717_like; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_region_pano_id_1d87b717_like ON public.panoramas_region USING btree (pano_id varchar_pattern_ops);
-- Name: panoramas_traject_geolocation_id; Type: INDEX; Schema: public; Owner: panorama
CREATE INDEX IF NOT EXISTS panoramas_traject_geolocation_id ON public.panoramas_traject USING gist (geolocation extensions.gist_geometry_ops_nd);

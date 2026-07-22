create or replace package {{THEME_PACKAGE}} authid definer as
    c_theme_id      constant varchar2(64) := '{{THEME_ID}}';
    c_theme_name    constant varchar2(120) := '{{THEME_NAME}}';
    c_theme_version constant varchar2(20) := '{{THEME_VERSION}}';

    function inline_css return clob;
    function logo_markup return clob;
end {{THEME_PACKAGE}};
/

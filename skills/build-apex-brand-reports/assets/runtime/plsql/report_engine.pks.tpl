create or replace package {{ENGINE_PACKAGE}} authid definer as
    c_runtime_version constant varchar2(20) := '0.1.0';

    procedure append(
        p_target in out nocopy clob,
        p_value  in clob
    );

    function html(p_value in varchar2) return varchar2;
    function attr(p_value in varchar2) return varchar2;
    function safe_filename(p_value in varchar2) return varchar2;

    function document_open(
        p_root_id           in varchar2,
        p_title             in varchar2,
        p_subtitle          in varchar2 default null,
        p_context           in varchar2 default null,
        p_orientation       in varchar2 default '{{ORIENTATION}}',
        p_header_variant    in varchar2 default '{{HEADER_VARIANT}}',
        p_header_size       in varchar2 default '{{HEADER_SIZE}}',
        p_toolbar_variant   in varchar2 default '{{TOOLBAR}}',
        p_toolbar_position  in varchar2 default '{{TOOLBAR_POSITION}}',
        p_density           in varchar2 default '{{DENSITY}}',
        p_economy_print     in boolean default {{ECONOMY_PRINT_BOOL}},
        p_repeat_table_head in boolean default {{REPEAT_TABLE_HEADER_BOOL}},
        p_suggested_name    in varchar2 default 'report.pdf',
        p_theme_css         in clob default null,
        p_logo_html         in clob default null,
        p_toolbar_html      in clob default null
    ) return clob;

    function document_close(
        p_footer_variant in varchar2 default '{{FOOTER_VARIANT}}',
        p_generated_at   in timestamp with time zone default systimestamp,
        p_generated_by   in varchar2 default null
    ) return clob;

    function section_open(
        p_title  in varchar2 default null,
        p_atomic in boolean default false
    ) return clob;

    function section_close return clob;

    function indicator(
        p_label in varchar2,
        p_value in varchar2,
        p_note  in varchar2 default null,
        p_tone  in varchar2 default 'neutral'
    ) return clob;

    function message(
        p_title in varchar2,
        p_text  in varchar2,
        p_tone  in varchar2 default 'info'
    ) return clob;

    function table_open(p_caption in varchar2 default null) return clob;
    function table_close return clob;
    function safe_error(p_reference in varchar2 default null) return clob;
end {{ENGINE_PACKAGE}};
/

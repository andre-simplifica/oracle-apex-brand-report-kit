-- Project-owned example. Add this function to the confirmed {{OWNER_PACKAGE}} body.
-- Replace synthetic composition only after confirming real queries, binds, and authorization.
function {{REPORT_FUNCTION}} return clob is
    l_html clob;
begin
    l_html := {{ENGINE_PACKAGE}}.document_open(
        p_root_id        => 'abrk-report-root',
        p_title          => '{{EXAMPLE_REPORT_TITLE}}',
        p_subtitle       => '{{EXAMPLE_REPORT_SUBTITLE}}',
        p_orientation    => '{{ORIENTATION}}',
        p_header_variant => '{{HEADER_VARIANT}}',
        p_header_size    => '{{HEADER_SIZE}}',
        p_toolbar_variant => '{{TOOLBAR}}',
        p_toolbar_position => '{{TOOLBAR_POSITION}}',
        p_density        => '{{DENSITY}}',
        p_economy_print  => {{ECONOMY_PRINT_BOOL}},
        p_repeat_table_head => {{REPEAT_TABLE_HEADER_BOOL}},
        p_suggested_name => '{{DEFAULT_FILENAME}}',
        p_theme_css      => {{THEME_PACKAGE}}.inline_css,
        p_logo_html      => {{THEME_PACKAGE}}.logo_markup
    );

    {{ENGINE_PACKAGE}}.append(l_html, {{ENGINE_PACKAGE}}.section_open('{{EXAMPLE_SUMMARY}}', true));
    {{ENGINE_PACKAGE}}.append(l_html, to_clob('<div class="abrk__indicators">'));
    {{ENGINE_PACKAGE}}.append(l_html, {{ENGINE_PACKAGE}}.indicator('{{EXAMPLE_METRIC}}', '0', '{{EXAMPLE_METRIC_NOTE}}'));
    {{ENGINE_PACKAGE}}.append(l_html, to_clob('</div>'));
    {{ENGINE_PACKAGE}}.append(l_html, {{ENGINE_PACKAGE}}.section_close);
    {{ENGINE_PACKAGE}}.append(l_html, {{ENGINE_PACKAGE}}.message('{{EXAMPLE_EMPTY_TITLE}}', '{{EXAMPLE_EMPTY_TEXT}}', 'info'));
    {{ENGINE_PACKAGE}}.append(l_html, {{ENGINE_PACKAGE}}.document_close(
        p_footer_variant => '{{FOOTER_VARIANT}}',
        p_generated_by   => v('APP_USER')
    ));
    return l_html;
exception
    when others then
        -- Log sanitized diagnostics through the project-approved mechanism.
        return {{ENGINE_PACKAGE}}.safe_error('REPORT');
end {{REPORT_FUNCTION}};

create or replace package body {{ENGINE_PACKAGE}} as
    function new_clob return clob is
        l_result clob;
    begin
        dbms_lob.createtemporary(l_result, true, dbms_lob.call);
        return l_result;
    end new_clob;

    procedure append_text(
        p_target in out nocopy clob,
        p_value  in varchar2
    ) is
    begin
        if p_value is not null then
            dbms_lob.writeappend(p_target, length(p_value), p_value);
        end if;
    end append_text;

    procedure append(
        p_target in out nocopy clob,
        p_value  in clob
    ) is
        l_offset pls_integer := 1;
        l_chunk  varchar2(32767);
    begin
        if p_value is null then
            return;
        end if;
        while l_offset <= dbms_lob.getlength(p_value) loop
            l_chunk := dbms_lob.substr(p_value, 32767, l_offset);
            append_text(p_target, l_chunk);
            l_offset := l_offset + length(l_chunk);
        end loop;
    end append;

    function html(p_value in varchar2) return varchar2 is
    begin
        return apex_escape.html(p_value);
    end html;

    function attr(p_value in varchar2) return varchar2 is
    begin
        return apex_escape.html_attribute(p_value);
    end attr;

    function allowed(
        p_value   in varchar2,
        p_allowed in varchar2,
        p_default in varchar2
    ) return varchar2 is
        l_value varchar2(100) := lower(trim(p_value));
    begin
        if instr('|' || p_allowed || '|', '|' || l_value || '|') > 0 then
            return l_value;
        end if;
        return p_default;
    end allowed;

    function safe_filename(p_value in varchar2) return varchar2 is
        l_value varchar2(255);
    begin
        l_value := regexp_replace(trim(p_value), '[^A-Za-z0-9._-]+', '-');
        l_value := regexp_replace(l_value, '-+', '-');
        l_value := trim(both '-' from l_value);
        if l_value is null then
            l_value := 'report.pdf';
        end if;
        return substr(l_value, 1, 120);
    end safe_filename;

    function base_css return clob is
        l_css clob := new_clob;
    begin
        append_text(l_css, q'~
<style data-abrk-runtime>
.abrk{--abrk-page-width:210mm;--abrk-page-height:297mm;--abrk-margin:14mm;box-sizing:border-box;color:var(--abrk-text,#172033);background:var(--abrk-page,#fff);font-family:var(--abrk-font,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif);line-height:1.45;max-width:var(--abrk-content-width,1180px);margin:0 auto;isolation:isolate;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.abrk *,.abrk *::before,.abrk *::after{box-sizing:border-box}
.abrk [hidden]{display:none!important}.abrk a{color:inherit}.abrk button{font:inherit}
.abrk__toolbar{align-items:center;background:var(--abrk-surface,#fff);border:1px solid var(--abrk-border,#d8deea);border-radius:var(--abrk-control-radius,8px);display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end;margin:0 0 12px;padding:8px;position:sticky;top:8px;z-index:20}
.abrk__action{align-items:center;background:var(--abrk-primary,#175cd3);border:1px solid transparent;border-radius:var(--abrk-control-radius,8px);color:var(--abrk-primary-text,#fff);cursor:pointer;display:inline-flex;gap:6px;min-height:40px;padding:8px 12px}
.abrk__action--quiet{background:transparent;border-color:var(--abrk-border,#d8deea);color:var(--abrk-text,#172033)}
.abrk__action:focus-visible{outline:3px solid var(--abrk-focus,#326fd1);outline-offset:2px}
.abrk[data-toolbar-variant="compact"] .abrk__action{font-size:.8125rem;min-height:34px;padding:5px 9px}
.abrk__document{min-width:0;width:100%}
.abrk__header{background:var(--abrk-header,#eaf2ff);border:1px solid var(--abrk-border,#d8deea);border-radius:var(--abrk-hero-radius,16px);margin-bottom:16px;overflow:hidden;padding:20px}
.abrk__header--none{display:none}.abrk__header--text{background:transparent;border:0;border-radius:0;padding:0 0 12px}.abrk__header--band{border-color:var(--abrk-brand-band,var(--abrk-primary,#175cd3));border-radius:0;border-width:0 0 4px;padding:16px 20px}.abrk__header--compact{padding:12px 16px}.abrk__header--hero{padding:28px}
.abrk__header--hero{background:var(--abrk-hero-background,var(--abrk-header,#eaf2ff));color:var(--abrk-primary-text,#fff)}.abrk__header--hero .abrk__subtitle,.abrk__header--hero .abrk__context{color:inherit;opacity:.88}
.abrk[data-header-size="small"] .abrk__header{padding:12px}.abrk[data-header-size="small"] .abrk__title{font-size:clamp(1.25rem,2.2vw,1.8rem)}.abrk[data-header-size="large"] .abrk__header{padding:28px}.abrk[data-header-size="large"] .abrk__title{font-size:clamp(1.8rem,3.5vw,3rem)}
.abrk__identity{align-items:center;display:flex;gap:16px}.abrk__logo{flex:0 0 auto}.abrk__title{font-size:clamp(1.5rem,3vw,2.5rem);line-height:1.1;margin:0}.abrk__subtitle{color:var(--abrk-muted,#526079);margin:8px 0 0}.abrk__context{font-size:.875rem;margin:8px 0 0}
.abrk__body{display:grid;gap:16px}.abrk__body>*{min-width:0}.abrk__section{background:var(--abrk-surface,#fff);border:1px solid var(--abrk-border,#d8deea);border-radius:var(--abrk-card-radius,14px);box-shadow:var(--abrk-card-shadow,none);padding:18px}.abrk__section[data-atomic="true"]{break-inside:avoid;page-break-inside:avoid}.abrk__section-title{font-size:1.125rem;margin:0 0 12px}
.abrk[data-density="compact"] .abrk__body{gap:10px}.abrk[data-density="compact"] .abrk__section{padding:12px}.abrk[data-density="compact"] .abrk__table th,.abrk[data-density="compact"] .abrk__table td{padding:6px 8px}.abrk[data-density="spacious"] .abrk__body{gap:22px}.abrk[data-density="spacious"] .abrk__section{padding:22px}.abrk[data-density="spacious"] .abrk__table th,.abrk[data-density="spacious"] .abrk__table td{padding:12px}
.abrk__indicators{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr))}.abrk__indicator{border-left:4px solid var(--abrk-primary,#175cd3);background:var(--abrk-soft,#f4f7fb);border-radius:10px;padding:14px;break-inside:avoid}.abrk__indicator[data-tone="success"]{border-color:var(--abrk-success,#067647)}.abrk__indicator[data-tone="warning"]{border-color:var(--abrk-warning,#b54708)}.abrk__indicator[data-tone="danger"]{border-color:var(--abrk-danger,#b42318)}
.abrk__indicator-label{color:var(--abrk-muted,#526079);font-size:.8rem}.abrk__indicator-value{font-size:1.65rem;font-weight:750;line-height:1.15;margin-top:4px}.abrk__indicator-note{color:var(--abrk-muted,#526079);font-size:.8rem;margin-top:5px}
.abrk__message{border:1px solid var(--abrk-border,#d8deea);border-radius:10px;padding:14px}.abrk__message[data-tone="error"]{background:var(--abrk-danger-soft,#fff1f0);border-color:var(--abrk-danger,#b42318)}.abrk__message-title{font-weight:700}.abrk__message p{margin:4px 0 0}
.abrk__table-wrap{max-width:100%;overflow:auto;width:100%}.abrk__table{border-collapse:collapse;font-variant-numeric:tabular-nums;width:100%}.abrk__table caption{font-weight:700;padding:0 0 8px;text-align:left}.abrk__table th,.abrk__table td{border-bottom:1px solid var(--abrk-border,#d8deea);padding:9px 10px;text-align:left;vertical-align:top}.abrk__table th{background:var(--abrk-table-head,#edf2fa);font-size:.8rem}.abrk__table thead{display:table-header-group}.abrk[data-repeat-table-header="false"] .abrk__table thead{display:table-row-group}.abrk__table tr{break-inside:avoid;page-break-inside:avoid}
.abrk__footer{color:var(--abrk-muted,#526079);font-size:.75rem;margin-top:14px;padding:8px 0}.abrk__footer--none{display:none}.abrk__footer-meta{display:flex;flex-wrap:wrap;gap:8px 18px;justify-content:space-between}
@media(max-width:640px){.abrk__toolbar{position:static}.abrk__action{flex:1 1 auto;justify-content:center}.abrk__header--hero{padding:20px}.abrk__identity{align-items:flex-start;flex-direction:column}.abrk__section{padding:14px}.abrk__table{min-width:640px}}
@media(prefers-reduced-motion:reduce){.abrk *{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}}
@media print{.abrk{--abrk-content-width:none;max-width:none}.abrk[data-economy-print="true"]{background:#fff!important;-webkit-print-color-adjust:economy;print-color-adjust:economy}.abrk[data-economy-print="true"] .abrk__header,.abrk[data-economy-print="true"] .abrk__section,.abrk[data-economy-print="true"] .abrk__indicator{background:transparent!important;box-shadow:none!important}.abrk__toolbar{display:none!important}.abrk__header{border-radius:0;margin-bottom:5mm}.abrk__section{box-shadow:none}.abrk__section:has(.abrk__table){border:0;border-radius:0;padding:0}.abrk__table-wrap{overflow:visible}.abrk__footer{margin-top:4mm}.abrk a{text-decoration:none}}
</style>
~');
        return l_css;
    end base_css;

    function runtime_js return clob is
        l_js clob := new_clob;
    begin
        append_text(l_js, q'~
<script data-abrk-runtime>
(function(w,d){"use strict";if(w.ApexBrandReportKit){w.ApexBrandReportKit.init(d);return;}
function roots(ctx){return Array.prototype.slice.call((ctx||d).querySelectorAll("[data-abrk-root]"));}
function activate(root,button){var action=button.getAttribute("data-abrk-action");if(action==="print"||action==="pdf"){w.print();return;}if(action==="fullscreen"){if(!d.fullscreenElement&&root.requestFullscreen){root.requestFullscreen();}else if(d.exitFullscreen){d.exitFullscreen();}return;}if(action==="xlsx"||action==="csv"){var request="ABRK_EXPORT_"+action.toUpperCase();var event=new CustomEvent("abrkexport",{bubbles:true,cancelable:true,detail:{format:action,request:request}});if(!root.dispatchEvent(event)){return;}if(w.apex&&typeof w.apex.submit==="function"){w.apex.submit({request:request,showWait:true});}}}
function bind(root){if(root.dataset.abrkBound==="true"){return;}root.dataset.abrkBound="true";root.addEventListener("click",function(event){var button=event.target.closest("[data-abrk-action]");if(button&&root.contains(button)){activate(root,button);}});}
function init(ctx){roots(ctx).forEach(bind);}w.ApexBrandReportKit={init:init};init(d);if(!d.documentElement.dataset.abrkRefreshBound){d.documentElement.dataset.abrkRefreshBound="true";d.addEventListener("apexafterrefresh",function(event){init(event.target);});}}
)(window,document);
</script>
~');
        return l_js;
    end runtime_js;

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
    ) return clob is
        l_result      clob := new_clob;
        l_orientation varchar2(20) := allowed(p_orientation, 'portrait|landscape', 'portrait');
        l_header      varchar2(20) := allowed(p_header_variant, 'none|text|band|compact|hero', 'text');
        l_header_size varchar2(20) := allowed(p_header_size, 'small|medium|large', 'medium');
        l_toolbar     varchar2(20) := allowed(p_toolbar_variant, 'none|compact|full|custom', 'full');
        l_toolbar_pos varchar2(20) := allowed(p_toolbar_position, 'above-header|inside-header|below-header', 'above-header');
        l_density     varchar2(20) := allowed(p_density, 'compact|comfortable|spacious', 'comfortable');
        l_has_actions boolean := {{FEATURE_FULLSCREEN}} or {{FEATURE_PRINT}} or {{FEATURE_PDF}} or {{FEATURE_XLSX}} or {{FEATURE_CSV}};
        procedure add_toolbar is
        begin
            if l_toolbar = 'none' or (l_toolbar = 'custom' and p_toolbar_html is null) or (l_toolbar <> 'custom' and not l_has_actions) then
                return;
            end if;
            append_text(l_result, '<div class="abrk__toolbar" role="toolbar" aria-label="Report actions">');
            if l_toolbar = 'custom' then
                append(l_result, p_toolbar_html);
                append_text(l_result, '</div>');
                return;
            end if;
            if {{FEATURE_FULLSCREEN}} then append_text(l_result, '<button class="abrk__action abrk__action--quiet" type="button" data-abrk-action="fullscreen">Full screen</button>'); end if;
            if {{FEATURE_PRINT}} then append_text(l_result, '<button class="abrk__action abrk__action--quiet" type="button" data-abrk-action="print">Print</button>'); end if;
            if {{FEATURE_PDF}} then append_text(l_result, '<button class="abrk__action" type="button" data-abrk-action="pdf">Save as PDF</button>'); end if;
            if {{FEATURE_XLSX}} then append_text(l_result, '<button class="abrk__action" type="button" data-abrk-action="xlsx">XLSX</button>'); end if;
            if {{FEATURE_CSV}} then append_text(l_result, '<button class="abrk__action abrk__action--quiet" type="button" data-abrk-action="csv">CSV</button>'); end if;
            append_text(l_result, '</div>');
        end add_toolbar;
    begin
        if l_header = 'none' and l_toolbar_pos = 'inside-header' then
            l_toolbar_pos := 'below-header';
        end if;
        append(l_result, base_css);
        append(l_result, p_theme_css);
        append_text(l_result, '<style data-abrk-page>@page{size:A4 ' || l_orientation || ';margin:14mm}</style>');
        append_text(l_result, '<div class="abrk" id="' || attr(p_root_id) || '" data-abrk-root data-orientation="' || attr(l_orientation) || '" data-header-size="' || attr(l_header_size) || '" data-toolbar-variant="' || attr(l_toolbar) || '" data-toolbar-position="' || attr(l_toolbar_pos) || '" data-density="' || attr(l_density) || '" data-economy-print="' || case when p_economy_print then 'true' else 'false' end || '" data-repeat-table-header="' || case when p_repeat_table_head then 'true' else 'false' end || '" data-suggested-name="' || attr(safe_filename(p_suggested_name)) || '">');
        if l_toolbar_pos = 'above-header' then add_toolbar; end if;
        append_text(l_result, '<div class="abrk__document">');
        append_text(l_result, '<header class="abrk__header abrk__header--' || attr(l_header) || '"><div class="abrk__identity">');
        if '{{SHOW_LOGO}}' = 'Y' and p_logo_html is not null then append_text(l_result, '<div class="abrk__logo">'); append(l_result, p_logo_html); append_text(l_result, '</div>'); end if;
        append_text(l_result, '<div><h1 class="abrk__title">' || html(p_title) || '</h1>');
        if p_subtitle is not null then append_text(l_result, '<p class="abrk__subtitle">' || html(p_subtitle) || '</p>'); end if;
        if p_context is not null then append_text(l_result, '<p class="abrk__context">' || html(p_context) || '</p>'); end if;
        append_text(l_result, '</div></div>');
        if l_toolbar_pos = 'inside-header' then add_toolbar; end if;
        append_text(l_result, '</header>');
        if l_toolbar_pos = 'below-header' then add_toolbar; end if;
        append_text(l_result, '<main class="abrk__body">');
        return l_result;
    exception
        when others then
            return safe_error('OPEN');
    end document_open;

    function document_close(
        p_footer_variant in varchar2 default '{{FOOTER_VARIANT}}',
        p_generated_at   in timestamp with time zone default systimestamp,
        p_generated_by   in varchar2 default null
    ) return clob is
        l_result clob := new_clob;
        l_footer varchar2(20) := allowed(p_footer_variant, 'none|compact|full', 'compact');
    begin
        append_text(l_result, '</main>');
        append_text(l_result, '<footer class="abrk__footer abrk__footer--' || attr(l_footer) || '"><div class="abrk__footer-meta">');
        if '{{SHOW_EMISSION_DATETIME}}' = 'Y' then append_text(l_result, '<span>Generated at ' || html(to_char(p_generated_at at time zone '{{TIMEZONE}}', 'YYYY-MM-DD HH24:MI TZH:TZM')) || '</span>'); end if;
        if '{{SHOW_EMISSION_USER}}' = 'Y' and p_generated_by is not null then append_text(l_result, '<span>Generated by ' || html(p_generated_by) || '</span>'); end if;
        append_text(l_result, '</div></footer></div></div>');
        append(l_result, runtime_js);
        return l_result;
    end document_close;

    function section_open(p_title in varchar2 default null, p_atomic in boolean default false) return clob is
        l_result clob := new_clob;
    begin
        append_text(l_result, '<section class="abrk__section" data-atomic="' || case when p_atomic then 'true' else 'false' end || '">');
        if p_title is not null then append_text(l_result, '<h2 class="abrk__section-title">' || html(p_title) || '</h2>'); end if;
        return l_result;
    end section_open;

    function section_close return clob is begin return to_clob('</section>'); end section_close;

    function indicator(p_label in varchar2, p_value in varchar2, p_note in varchar2 default null, p_tone in varchar2 default 'neutral') return clob is
        l_result clob := new_clob;
        l_tone varchar2(20) := allowed(p_tone, 'neutral|success|warning|danger', 'neutral');
    begin
        append_text(l_result, '<article class="abrk__indicator" data-tone="' || attr(l_tone) || '"><div class="abrk__indicator-label">' || html(p_label) || '</div><div class="abrk__indicator-value">' || html(p_value) || '</div>');
        if p_note is not null then append_text(l_result, '<div class="abrk__indicator-note">' || html(p_note) || '</div>'); end if;
        append_text(l_result, '</article>');
        return l_result;
    end indicator;

    function message(p_title in varchar2, p_text in varchar2, p_tone in varchar2 default 'info') return clob is
        l_tone varchar2(20) := allowed(p_tone, 'info|success|warning|error', 'info');
    begin
        return to_clob('<aside class="abrk__message" data-tone="' || attr(l_tone) || '" role="status"><div class="abrk__message-title">' || html(p_title) || '</div><p>' || html(p_text) || '</p></aside>');
    end message;

    function table_open(p_caption in varchar2 default null) return clob is
        l_result clob := new_clob;
    begin
        append_text(l_result, '<div class="abrk__table-wrap"><table class="abrk__table">');
        if p_caption is not null then append_text(l_result, '<caption>' || html(p_caption) || '</caption>'); end if;
        return l_result;
    end table_open;

    function table_close return clob is begin return to_clob('</table></div>'); end table_close;

    function safe_error(p_reference in varchar2 default null) return clob is
        l_reference varchar2(100) := regexp_replace(p_reference, '[^A-Za-z0-9._-]', '');
    begin
        return to_clob('<div class="abrk"><aside class="abrk__message" data-tone="error" role="alert"><div class="abrk__message-title">Report unavailable</div><p>We could not prepare this report. Please try again or contact support' || case when l_reference is not null then ' and mention reference ' || attr(l_reference) else null end || '.</p></aside></div>');
    end safe_error;
end {{ENGINE_PACKAGE}};
/

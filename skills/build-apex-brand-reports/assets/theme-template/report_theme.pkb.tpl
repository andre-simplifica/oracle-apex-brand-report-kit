create or replace package body {{THEME_PACKAGE}} as
    function inline_css return clob is
    begin
        return to_clob(q'~<style data-abrk-theme>
.abrk{--abrk-primary:{{COLOR_PRIMARY}};--abrk-primary-text:{{COLOR_PRIMARY_TEXT}};--abrk-surface:{{COLOR_SURFACE}};--abrk-page:{{COLOR_PAGE}};--abrk-text:{{COLOR_TEXT}};--abrk-muted:{{COLOR_MUTED}};--abrk-border:{{COLOR_BORDER}};--abrk-success:{{COLOR_SUCCESS}};--abrk-warning:{{COLOR_WARNING}};--abrk-danger:{{COLOR_DANGER}};--abrk-danger-text:{{COLOR_DANGER_TEXT}};--abrk-focus:{{COLOR_FOCUS}};--abrk-header:{{HEADER_BACKGROUND}};--abrk-hero-background:{{HERO_BACKGROUND}};--abrk-brand-band:{{BRAND_BAND_BACKGROUND}};--abrk-soft:{{SOFT_BACKGROUND}};--abrk-table-head:{{TABLE_HEADER_BACKGROUND}};--abrk-card-radius:{{CARD_RADIUS}};--abrk-control-radius:{{CONTROL_RADIUS}};--abrk-hero-radius:{{HERO_RADIUS}};--abrk-card-shadow:{{CARD_SHADOW}};--abrk-font:{{FONT_FAMILY}};--abrk-content-width:{{CONTENT_WIDTH}}}
</style>~');
    end inline_css;

    function logo_markup return clob is
    begin
        -- Replace this text mark only with an original, licensed consumer asset.
        return to_clob('<span role="img" aria-label="{{THEME_NAME}}" style="font-weight:800">{{THEME_NAME}}</span>');
    end logo_markup;
end {{THEME_PACKAGE}};
/

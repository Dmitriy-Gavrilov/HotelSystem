#ifndef DEPARTFORM_H
#define DEPARTFORM_H

#include <QWidget>

#include "baseform.h"

namespace Ui {
class DepartForm;
}

class DepartForm : public QWidget, public BaseForm
{
    Q_OBJECT

public:
    explicit DepartForm(QWidget *parent = nullptr);
    ~DepartForm();

    void clear() override;

signals:
    void sendData(const QString &data);

private slots:
    void on_pushButton_clicked();

private:
    Ui::DepartForm *ui;
};

#endif // DEPARTFORM_H

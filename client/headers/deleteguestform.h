#ifndef DELETEGUESTFORM_H
#define DELETEGUESTFORM_H

#include <QWidget>

#include "baseform.h"

namespace Ui {
class DeleteGuestForm;
}

class DeleteGuestForm : public QWidget, public BaseForm
{
    Q_OBJECT

public:
    explicit DeleteGuestForm(QWidget *parent = nullptr);
    ~DeleteGuestForm();

    void clear() override;
signals:
    void sendData(const QString &data);

private slots:
    void on_deleteGuestBtn_clicked();

private:
    Ui::DeleteGuestForm *ui;
};

#endif // DELETEGUESTFORM_H
